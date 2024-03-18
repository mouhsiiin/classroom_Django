from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def dashboard(request):
    return render(request, "classrooms/dashboard.html")


@login_required
def create_class(request):
    return render(request, "classrooms/create_class.html")