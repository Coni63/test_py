from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import AViewSet, BViewSet, CViewSet, TotalProductSales
from .views import MyProtectedView


router = DefaultRouter()
# router.register(r'a', AViewSet)
# router.register(r'b', BViewSet)
# router.register(r'c', CViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path("d", TotalProductSales.as_view())
    path('my-api/', MyProtectedView.as_view(), name='my-api'),
]