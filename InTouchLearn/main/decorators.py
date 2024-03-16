from django.shortcuts import  redirect
from functools import wraps
from main.models import User

def require_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        user = User.objects.filter(id=request.session.get("user_id")).first()
        if not request.session.get("user_id") or user.is_email_verified == False:
            print("User not authenticated. Redirecting to login.")
            return redirect("login")

        return func(request, *args, **kwargs)

    return wrapper
