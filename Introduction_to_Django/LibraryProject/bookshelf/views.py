from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.
def hello_view(request):
    return HttpResponse("This is my store")

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, books/book_list.html, context)


# creating a signup view
class SignUp(CreateView):
    form = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def profile_view(request):
    return render(request, 'profile.html')