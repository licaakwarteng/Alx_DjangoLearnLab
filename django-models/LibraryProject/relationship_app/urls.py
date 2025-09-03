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
    path("admin-dashboard/", views.admin_view, name="admin_view"),
    path("librarian-dashboard/", views.librarian_view, name="librarian_view"),
    path("member-dashboard/", views.member_view, name="member_view"),
]
