from django.db import models

# Creating models Author and Book.
class Author(models.Model):
    name = models.CharField()

# Book model contains a foreign key from Author model
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
