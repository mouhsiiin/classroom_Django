from django.shortcuts import render
from main.decorators import require_login


@require_login
def home(request):
    print("Home page")
    return render(request, "socialmedia/home.html", {})
