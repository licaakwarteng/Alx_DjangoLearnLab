from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter

#setting up a router
router = DefaultRouter()

# Register the BookViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]
