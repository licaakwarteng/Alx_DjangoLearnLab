from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager for CustomUser with email as required field."""

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError(_("Superuser must have a password"))
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username








# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class UserProfile(models.Model):
#     ROLE_CHOICES = [
#         ("Admin", "Admin"),
#         ("Librarian", "Librarian"),
#         ("Member", "Member"),
#     ]

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

#     def __str__(self):
#         return f"{self.user.username} - {self.role}"


# # --- Signals: auto-create/save profile for each new User ---
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()


# # Create your models here.
# class Author(models.Model):
#     name = models.CharField()

#     def __str__(self):
#         return self.name

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=200)
#     published_date = models.DateField()

#     def __str__(self):
#         return self.title

#     class Meta:
#         permissions = [
#             ("can_add_book", "Can add a book"),
#             ("can_change_book", "Can change a book"),
#             ("can_delete_book", "Can delete a book"),
#         ]

# class Library(models.Model):
#     name = models.CharField()
#     books = models.OneToOneField(Book, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class Librarian(models.Model):
#     name = models.CharField()
#     library = models.OneToOneField(Library, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name