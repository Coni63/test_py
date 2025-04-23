from django.urls import path
from .views import PersonListView, exchange_code_for_token

urlpatterns = [
    path('people/', PersonListView.as_view(), name='person-list'),
    path('login', exchange_code_for_token, name='login'),
]