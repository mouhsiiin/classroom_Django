from django.urls import path
from main import views
from socialmedia import views as social_views


urlpatterns = [
    path("", social_views.post_list_view , name="post-list"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("confirm_email/<uidb64>/<token>", views.confirm_email, name="confirm_email"),

]
