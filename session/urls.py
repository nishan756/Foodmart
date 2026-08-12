from django.urls import path
from .views import user_login , user_logout , user_signup , user_delete

urlpatterns = [
    path("user_signup/" , user_signup , name = "signup"),
    path("user_login/" , user_login , name = "login"),
    path("user_logout/" , user_logout , name = "logout"),
    path("user_delete/" , user_delete , name = "user-delete"),
]
