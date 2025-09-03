from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("books/", views.list_books, name="list_book"),  # function-based
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),  # class-based
    path("register/", views.register_view, name="register"),
    path("login/",LoginView.as_view(template_name="relationship_app/login.html"),name="login"),
    path("logout/",LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Role-based views
    path("Admin/", views.Admin, name="admin_view"),
    path("Librarian/", views.Librarian, name="librarian_view"),
    path("Member/", views.Member, name="member_view"),
    path("redirect/", views.role_redirect_view, name="role_redirect"),

    # Book management with permissions
    path("books/add_book/", views.add_book, name="add_book"),
    path("books/edit_book/<int:book_id>/", views.edit_book, name="edit_book"),
    path("books/delete/<int:book_id>/", views.delete_book, name="delete_book"),
]
