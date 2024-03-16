from django.db import models
from django.contrib.auth.models import AbstractUser as abstractUser
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

  


class  User(abstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField( _('email_verified'), default=False, help_text=_('Designates whether the user has verified their email address.'))

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  # Add this line
        related_query_name='user',  # And this line
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Add this line
        related_query_name='user',  # And this line
    )