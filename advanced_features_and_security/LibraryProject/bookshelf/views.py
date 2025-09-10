from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm
from django.shortcuts import render, redirect


def create_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()   # ✅ works if ExampleForm is a ModelForm
            return redirect("book_list")
    else:
        form = ExampleForm()

    return render(request, "books/book_form.html", {"form": form})

def search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(title__icontains=query)  # ✅ ORM prevents SQL injection
    return render(request, "books/book_list.html", {"books": books})

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    return HttpResponse("📖 Book creation page (only for users with can_create).")

@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"✏️ Edit page for {book.title} (only for users with can_edit).")

@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"🗑️ Delete page for {book.title} (only for users with can_delete).")
