from django.urls import path
from classrooms import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create_class/", views.create_class, name="create_class"),
]