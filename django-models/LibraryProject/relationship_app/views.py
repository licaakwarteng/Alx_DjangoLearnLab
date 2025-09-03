from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    
    # Option 1: Plain text response
    # output = ", ".join([f"{book.title} by {book.author.name}" for book in books])
    # return HttpResponse(output)

    # Option 2: Render using template
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: show details of a library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context


# Register View
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect("list_books")  # redirect to books page after signup
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


# Logout View
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


from django.contrib.auth.decorators import user_passes_test, login_required

# Role check functions
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# Views restricted by role
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
@login_required
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
@login_required
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@login_required
def role_redirect_view(request):
    """Redirect users to their dashboard based on role"""
    role = request.user.userprofile.role

    if role == "Admin":
        return redirect("admin_view")
    elif role == "Librarian":
        return redirect("librarian_view")
    else:  # Default to Member
        return redirect("member_view")