from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentSerializer
from .permissions import DocumentPermission, IsOwnerOrReadOnly, MyDjangoModelPermissions, CustomDjangoModelPermissions
from rest_framework.response import Response


class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [MyDjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [MyDjangoModelPermissions]


class DocumentToggleView(views.APIView):
    permission_classes = [CustomDjangoModelPermissions]
    queryset = Document.objects.all()  # Not required for APIView but ensures compatibility

    def post(self, request, pk, **kwargs):
        # Retrieve the document
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the private status
        document.is_private = not document.is_private
        document.save()

        return Response(
            {'message': 'Document status updated', 'is_private': document.is_private},
            status=status.HTTP_200_OK
        )