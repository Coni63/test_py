# from django.shortcuts import render
# from rest_framework import viewsets
# from .models import A, B, C
# from .serializer import ASerializer, BSerializer, CSerializer

# # Create your views here.

# class AViewSet(viewsets.ModelViewSet):
#     queryset = A.objects.all()
#     serializer_class = ASerializer

# class BViewSet(viewsets.ModelViewSet):
#     queryset = B.objects.all()
#     serializer_class = BSerializer

# class CViewSet(viewsets.ModelViewSet):
#     queryset = C.objects.all()
#     serializer_class = CSerializer



# # in views.py
# from django.db.models import Sum, Count
# from slick_reporting.views import ReportView, Chart
# from slick_reporting.fields import ComputationField
# from .models import Status

# # https://github.com/RamezIssac/django-slick-reporting

# class TotalProductSales(ReportView):
#     report_model = Status
#     date_field = "created_at"
#     group_by = "status"
#     time_series_pattern = "daily"
#     columns = [
#         # "message_id",
#         # "documentum_id",
#         # "publication_id",
#         # ComputationField.create(
#         #     Sum, "quantity", verbose_name="Total quantity sold", is_summable=False
#         # ),
#         # ComputationField.create(
#         #     Sum, "value", name="sum__value", verbose_name="Total Value sold $"
#         # ),
#         # ComputationField.create(Count, "message_id", name="count__message_id", verbose_name="Count")
#     ]

#     chart_settings = [
#         # Chart(
#         #     "Total sold $",
#         #     Chart.BAR,
#         #     data_source=["sum__value"],
#         #     title_source=["name"],
#         # ),
#         # Chart(
#         #     "Total sold $ [PIE]",
#         #     Chart.PIE,
#         #     data_source=["sum__value"],
#         #     title_source=["name"],
#         # ),
#     ]


from sample.models import Test
from sample.serializer import TestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .permissions import IsInGroup
# Filteirng
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import TextField


class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsInGroup]

    def get(self, request):
        return Response({"message": "Hello, {}!".format(request.user.username)})
    


# Custom pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total_records': Test.objects.count(),  # Total records in database
            'matching_records': self.page.paginator.count,  # Records after filtering
            'start': (self.page.number - 1) * self.page_size,  # Start index
            'size': self.page_size,  # Number of records per page
            'current_page': self.page.number,  # Current page number
            'total_pages': self.page.paginator.num_pages,  # Total number of pages
            'results': data
        })

# Filter class for Test model
class TestFilter(filters.FilterSet):
    id_like = filters.CharFilter(field_name='id', lookup_expr='istartswith')
    search = filters.CharFilter(method='search_fields')
    text = filters.CharFilter(lookup_expr='icontains')
    date_after = filters.DateTimeFilter(field_name='date', lookup_expr='gte', input_formats=["%Y-%m-%d"])
    date_before = filters.DateTimeFilter(field_name='date', lookup_expr='lte', input_formats=["%Y-%m-%d"])
    bool = filters.BooleanFilter()
    number_min = filters.NumberFilter(field_name='number', lookup_expr='gte')
    number_max = filters.NumberFilter(field_name='number', lookup_expr='lte')
    float_min = filters.NumberFilter(field_name='float', lookup_expr='gte')
    float_max = filters.NumberFilter(field_name='float', lookup_expr='lte')

    def search_fields(self, queryset, name, value):
        return queryset.annotate(
            id_as_text=Cast('id', TextField())
        ).filter(
            Q(id_as_text__istartswith=value) |
            Q(text__icontains=value)
        )

    class Meta:
        model = Test
        fields = ['id', 'text', 'bool', 'number', 'float']

class TestView(ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TestFilter
    # search_fields = ['text']
    ordering_fields = ['date', 'number', 'float']
    ordering = ['-date']  # Default ordering