#creating a decorator for login required

from django.shortcuts import redirect
from django.contrib.auth.models import User
from functools import wraps

def require_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return func(request, *args, **kwargs)
    return wrapper