from django.shortcuts import render , redirect
from django.contrib.auth import logout , login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from werkzeug.routing import ValidationError
from django.utils.http import url_has_allowed_host_and_scheme

# ==========Forms============
from .forms import LoginForm , SignupForm , CustomPasswordChangeForm

# =========Backend============
from .backends import CustomBackend

# ========Service=============
from .service import UserService
from core.services.email import EmailService

# =======Exceptions===========
from core.exceptions import ObjectAlreadyExists

from django.http import JsonResponse

import json

import threading



def user_signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = SignupForm(data=request.POST,files=request.FILES)


        if form.is_valid():

            try:
                UserService().create_user(form.cleaned_data)

            except ObjectAlreadyExists as e:
                messages.info(request, str(e))

            except Exception as e:
                messages.error(request , "Something went wrong")

            else:
                messages.success(request , "Successfully created your account. Please login")

                return redirect("login")

    else:
        form = SignupForm()

    return render(request , "signup.html" , {"form": form})

def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm()

    if request.method == "POST":
        data = json.loads(request.body)

        redirect_url = data.get("redirect_url" , "/home")

        if not url_has_allowed_host_and_scheme(redirect_url , request.get_host()):
            redirect_url = "/home"

        form = LoginForm(data={
            "username": data.get("username"),
            "password": data.get("password"),
        })

        if form.is_valid():
            username = data.get("username")
            password = data.get("password")
            user = CustomBackend().authenticate(request , username = username , password = password)
            if user:
                login(request , user)
                messages.success(request , "Login Successfull")
                return JsonResponse({"success":True , "redirect_url":redirect_url, "tags":"success"})
            
            return JsonResponse({"message":"Invalid Credentials" , "success":False , "tags":"info"})
        return JsonResponse({"message":"Invalid form data" , "tags":"warning"})

    return render(request , "login.html" , {"form":form})


def user_logout(request):
    logout(request)
    messages.success(request , "Logout successfull")
    return redirect("home")

@login_required(login_url = "login")
def user_delete(request):
    try:
        UserService().user_delete(request.user)

    except Exception as e:
        messages.error(request , "An exception occured while processing your request")

    else:
        messages.success(request , "We're sorry to see you go")
        return redirect('home')

@login_required(login_url = "login")
def change_password(request):
    form = CustomPasswordChangeForm(request.user)
    if request.method == "POST":

        data = json.loads(request.body)

        old_password = data.get("old_password")

        new_password1 = data.get("new_password1")

        new_password2 = data.get("new_password2")

        if new_password1 != new_password2:
            return JsonResponse({"success": False, "message": "New passwords do not match"})

        form = CustomPasswordChangeForm(user=request.user, data=data)

        if form.is_valid():
            try:
                UserService().change_password(
                    user=request.user,
                    old_password=old_password,
                    new_password=new_password1,
                )
                messages.success(request, "Password changed successfully")

                kwargs = {
                    "subject" : "Your password has changed" , 
                    "email_to" : [request.user.email] , 
                    "template_name" : "email/change-password.html",
                    "context":{
                        "user":request.user,
                        "body" : "We noticed your password has changed. If you doesn't make this action, please reset your password." , 
                    }
                }
                email_thread = threading.Thread(target = EmailService.send_email , kwargs = kwargs)

                email_thread.start()

                return JsonResponse({"success": True})
            
            except ValidationError as e:
                messages.error(request, str(e))
            
        return JsonResponse({"success": False, "message": "Invalid form data"})
    return render(request , "change-password.html" , {"form":form})

