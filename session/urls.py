from django.urls import path
from .views import user_login , user_logout , user_signup , user_delete

urlpatterns = [
    path("user-signup/" , user_signup , name = "signup"),
    path("user-login/" , user_login , name = "login"),
    path("user-logout/" , user_logout , name = "logout"),
    path("user-delete/" , user_delete , name = "user-delete"),
]
