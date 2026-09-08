from django.shortcuts import render , redirect
from django.contrib.auth import logout , login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ==========Forms============
from .forms import LoginForm , SignupForm

# =========Backend============
from .backends import CustomBackend

# ========Service=============
from .service import UserService

# =======Exceptions===========
from core.exceptions import ObjectAlreadyExists

from django.http import JsonResponse

import json


user_service = UserService()


def user_signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = SignupForm(data=request.POST,files=request.FILES)


        if form.is_valid():

            try:
                user_service.create_user(form.cleaned_data)

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
                return JsonResponse({"success":True , "redirect_url":request.GET.get("next" , "/"), "tags":"success"})
            
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
        user_service.user_delete(request.user)

    except Exception as e:
        messages.error(request , "An exception occured while processing your request")

    else:
        messages.success(request , "We're sorry to see you go")
        return redirect('home')

