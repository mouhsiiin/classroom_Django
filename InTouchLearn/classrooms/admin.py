from django.contrib import admin

from .models import Classrooms, Students, Teachers , Assignments, Submissions, CourseContent

admin.site.register(Classrooms)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Assignments)
admin.site.register(Submissions)

