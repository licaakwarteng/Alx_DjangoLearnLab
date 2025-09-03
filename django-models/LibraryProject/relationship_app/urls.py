from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="list_book"),  # function-based
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),  # class-based
]
