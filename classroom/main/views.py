from django.shortcuts import render
from django.shortcuts import redirect

from main.models import virtual_class, User
import string
import random
from main.decorators import require_login

@require_login
def dashboard(request):
    classes = virtual_class.objects.filter(admin=request.user)
    return render(request, "main/dashboard.html", {"classrooms": classes})

def login(request):
    return render(request, "main/login.html", {})

def register(request):
    if request.method == "POST":
        if not request.POST.get("username"):
            return render(request, "main/register.html", {"message": "Username required."})
        if not request.POST.get("email"):
            return render(request, "main/register.html", {"message": "Email required."})
        if not request.POST.get("password"):
            return render(request, "main/register.html", {"message": "Password required."})
        new_user = User(
            username=request.POST["username"],
            email=request.POST["email"],
            password=hash(request.POST["password"])
        )
        new_user.save()
        return redirect("login")
    return render(request, "main/register.html", {})

def create_class(request):

    if request.method == "POST":
        if not request.POST.get("class_name"):
            return render(request, "main/create_class.html", {"message": "Class name required."})
        random_6_char = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_class = virtual_class(
            class_name=request.POST["class_name"],
            class_code=random_6_char,
            admin=request.user
        )
        if request.POST.get("members"):
            for member in request.POST["members"].split(","):
                new_class.class_members.add(member)
        new_class.save()
        return redirect("dashboard", {"message": "Class created successfully."})
    
    return render(request, "main/create_class.html", {})



