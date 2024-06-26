from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, default='student')
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', blank=True, null=True, default='uploads/profile_pictures/default.jpg')
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.username
    
    def is_teacher(self):
        return self.role == 'teacher'

    def is_enterprise(self):
        return self.role == 'enterprise'