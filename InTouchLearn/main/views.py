from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

from main.models import  User
import string
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.hashers import  make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required



def home(request):
    #if the user is authenticated redirect him to the post list
    if request.user.is_authenticated:
        return redirect("socialmedia:post-list")
    return redirect("socialmedia:landing")

def login(request):
    error = None
    if request.method == "POST":
        if not request.POST.get("email"):
            return render(request, "main/login.html", {"error": "Email required."})
        if not request.POST.get("password"):
            return render(request, "main/login.html", {"error": "Password required."})
        
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Check if the provided email exists in the database
        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, "main/login.html", {"error": "User not found."})

        # Use authenticate to verify the credentials
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if user.is_active:
                if user.is_email_verified:
                    # Log the user in
                    #clearing the session
                    request.session.clear()
                    request.session["user_id"] = user.id
                    print("User loging in")
                    auth_login(request, user)
                    print("User loged in")
                    return redirect("socialmedia:post-list")
                else:
                    messages.error(request, "Please verify your email to login.")
            else:
                messages.error(request, "Your account is disabled.")
        else:
            messages.error(request, "Invalid email or password.")

        #casting the messages to list
        error = list(messages.get_messages(request))
        print(type(error))


    return render(request, "main/login.html", {"error": error if error else None})



def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not username:
            return render(request, "main/register.html", {"error": "Username required."})
        if not email:
            return render(request, "main/register.html", {"error": "Email required."})
        
        if role == "student" and email.split("@")[1] != "etu.uae.ac.ma" :
            return render(request, "main/register.html", {"error": "Email must be a student email."})
        if role == "teacher" and email.split("@")[1] != "uae.ac.ma" :
            return render(request, "main/register.html", {"error": "Email must be a teacher email."})
        
        if not password:
            return render(request, "main/register.html", {"error": "Password required."})
        if User.objects.filter(email=email).exists():
            return render(request, "main/register.html", {"error": "Email already exists."})
        if User.objects.filter(username=username).exists():
            return render(request, "main/register.html", {"error": "Username already exists."})
        if len(password) < 8:
            return render(request, "main/register.html", {"error": "Password must be at least 8 characters long."})

        # Use make_password to securely hash the password
        hashed_password = make_password(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
        
        )
        new_user.save()

        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'uidb64': uid, 'token': token}))

        send_mail(
            'Confirm your email',
            f'Click the link to confirm your email: {confirmation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return render(request, "main/confirm_email.html", {"message": "Confirmation email sent."})
    
    return render(request, "main/register.html", {})


def confirm_email(request, uidb64, token):
    print(User.objects.all())
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(user)
    print(token)
    print(uidb64, "==>", uid)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return redirect("login")
    else:
        return render(request, "main/confirm_email.html", {"error": "Invalid confirmation link."})


def logout(request):
    request.session.clear()
    return redirect("login")

