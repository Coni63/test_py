# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Person
from .serializers import PersonSerializer

class PersonListView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer