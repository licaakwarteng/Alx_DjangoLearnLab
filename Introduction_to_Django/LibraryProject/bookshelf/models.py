from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()

# #Create a new user
# user = User.objects.create('angelica', 'angie@email.com', 'password123')

# # Retrieve a user based on username
# user = User.objects.get(username='angelica')