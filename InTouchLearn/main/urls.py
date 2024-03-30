from django.urls import path
from main import views
from socialmedia import views as social_views


urlpatterns = [
    path("", social_views.post_list_view , name="post-list"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/logout/", views.logout, name="logout"),
    path("confirm_email/<uidb64>/<token>", views.confirm_email, name="confirm_email"),

]
