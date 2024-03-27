from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class virtual_class(models.Model):
    class_name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    class_description = models.TextField()
    class_members = models.ManyToManyField("User", related_name="classes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey("User", on_delete=models.CASCADE, related_name="admin_classes")



class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.username