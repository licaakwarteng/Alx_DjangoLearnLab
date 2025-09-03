from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.username} - {self.role}"
    

# Create your models here.
class Author(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField()
    books = models.OneToOneField(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField()
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name