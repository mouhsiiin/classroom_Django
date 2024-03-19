from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings

from main.models import virtual_class, User
import string
import random
from main.decorators import require_login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages




def login(request):
    if request.method == "POST":
        if not request.POST.get("username"):
            return render(request, "main/login.html", {"error": "Username required."})
        if not request.POST.get("password"):
            return render(request, "main/login.html", {"error": "Password required."})
        
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Get the user with the provided username
        user = User.objects.filter(username=username).first()

        if not user:
            return render(request, "main/login.html", {"error": "User not found."})

        # Use check_password to verify the entered password against the hashed password
        print(password, "==>", user.password , "==>", check_password(password, user.password))
        if not check_password(password, user.password):
            return render(request, "main/login.html", {"error": "Incorrect password."})

        request.user = user
        print(request.user.is_authenticated)

        print("Login View - Session Data:", request.session.items())


        request.session["user_id"] = user.id
        return redirect("home")

    return render(request, "main/login.html", {})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username:
            return render(request, "main/register.html", {"error": "Username required."})
        if not email:
            return render(request, "main/register.html", {"error": "Email required."})
        if not password:
            return render(request, "main/register.html", {"error": "Password required."})

        # Use make_password to securely hash the password
        hashed_password = make_password(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
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

@require_login
def create_class(request):

    if request.method == "POST":
        print("create_class POST request:", request.POST)
        print(request.user)
        if not request.POST.get("class_name"):
            return render(request, "main/create_class.html", {"message": "Class name required."})
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
    
    return render(request, "main/create_class.html", {})

def logout(request):
    request.session.clear()
    return redirect("login")

