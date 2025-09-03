from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view: list all books
def book_list(request):
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
