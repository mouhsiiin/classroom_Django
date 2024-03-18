from django.urls import path
from socialmedia import views


urlpatterns = [
    path("", views.home, name="home"),
]