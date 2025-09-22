from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_books = ('title', 'author', 'publication_year')
    search_books = ('title', 'author')

admin.site.register(Book, BookAdmin)