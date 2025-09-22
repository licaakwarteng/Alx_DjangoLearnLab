from django.urls import path, include
from . import views

urlpatterns = [
    path('books/', views.book_list, name='books'),
]