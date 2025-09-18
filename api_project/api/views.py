from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import BookSerializer, Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


    # Apply permissions
    permission_classes = [IsAuthenticated]  # All users need to be authenticated for this view

    def get_permissions(self):
        """
        Override the default permissions for the update and delete actions.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Only admins can update or delete books
        return super().get_permissions()