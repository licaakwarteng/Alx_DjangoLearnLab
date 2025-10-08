from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    # followers: ManyToMany to self, non-symmetrical
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)


    def __str__(self):
        return self.username
    
