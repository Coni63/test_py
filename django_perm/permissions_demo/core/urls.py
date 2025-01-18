from django.urls import path
from .views import DocumentListCreateView, DocumentRetrieveUpdateDestroyAPIView, DocumentToggleView

urlpatterns = [
    path('documents/', DocumentListCreateView.as_view(), name='docs'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDestroyAPIView.as_view(), name='docs2'),
    path('documents/<int:pk>/private/', DocumentToggleView.as_view(), name='docs3'),
]