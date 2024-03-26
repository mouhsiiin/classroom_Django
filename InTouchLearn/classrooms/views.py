from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import virtual_class
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import User
import random
import string
from django.contrib import messages


@login_required
def dashboard(request):
    classes = virtual_class.objects.all()
    context = {
        "classes": classes
    }
    return render(request, "classrooms/dashboard.html", context)


@login_required
def create_class(request):

    if request.method == "POST":
        print("create_class POST request:", request.POST)
        print(request.user)
        if not request.POST.get("class_name"):
            return render(request, "classrooms/create_class.html", {"message": "Class name required."})
        random_6_char = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user = User.objects.get(id=request.session.get("user_id"))
        new_class = virtual_class(
            class_name=request.POST["class_name"],
            class_code=random_6_char,
            admin=user
        )
        if request.POST.get("members"):
            for member in request.POST["members"].split(","):
                new_class.class_members.add(member)
        new_class.save()
        messages.success(request, 'Class created successfully.')
        return redirect(reverse('dashboard'))
    
    return render(request, "classrooms/create_class.html", {})
