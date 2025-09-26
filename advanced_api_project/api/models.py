from django.db import models

# Creating models Author and Book.
class Author(models.Model):
    name = models.CharField(max_length=100)

#adding a foreign key to model Book.
class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)