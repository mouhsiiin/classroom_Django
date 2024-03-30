from django.contrib import admin

from .models import Classrooms, Students, Teachers

admin.site.register(Classrooms)
admin.site.register(Students)
admin.site.register(Teachers)
