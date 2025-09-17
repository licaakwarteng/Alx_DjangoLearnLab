from django.db import models

# Create your models here.
class Book():
    title = models.CharField()
    author = models.CharField()