from django.contrib import admin

# Register your models here.
from .models import virtual_class, User

admin.site.register(virtual_class)
admin.site.register(User)
