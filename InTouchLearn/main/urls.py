from django.urls import path
from main import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("create_class/", views.create_class, name="create_class"),
    path("logout/", views.logout, name="logout"),
    path("confirm_email/<uidb64>/<token>", views.confirm_email, name="confirm_email"),
]