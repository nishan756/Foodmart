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
from common.exceptions import ObjectAlreadyExists


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

    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = CustomBackend().authenticate(request , username = username , password = password)
            if user:
                login(request , user)
                messages.success(request , "Login successfull")
                return redirect("home")
            messages.info(request , "Invalid credentials")
            return redirect("login")

    form = LoginForm()
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

