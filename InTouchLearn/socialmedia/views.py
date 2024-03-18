from django.shortcuts import render



def home(request):
    print("Home page")
    return render(request, "socialmedia/home.html", {})
