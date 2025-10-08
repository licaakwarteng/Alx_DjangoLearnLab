from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
# from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    """
    GET /books/ - List all books.
    Open to all users (read-only).

    - Supports filtering by 'title', 'author', and 'publication_year'.
    e.g., /api/books/?author=1
    - Supports search by 'title' and author's name.
    e.g., /api/books/?search=tolkien
    - Supports ordering by 'title' or 'publication_year'.
    e.g., /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only, open access
    #filtering books
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year'] #ordering search by fields

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/ - Retrieve a single book by ID.
    Open to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/ - Create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/<pk>/ - Update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/ - Delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    

    