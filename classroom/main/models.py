from django.db import models

# Create your models here.


class virtual_class(models.Model):
    class_name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    class_description = models.TextField()
    class_members = models.ManyToManyField("User", related_name="classes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey("User", on_delete=models.CASCADE, related_name="admin_classes")



class  User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
