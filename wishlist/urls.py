from django.urls import path
from .views import add_to_wishlist , delete_from_wishlist , my_wishlist

urlpatterns = [
    path("my-wishlist/" , my_wishlist , name = "my-wishlist"),
    path("add/<uuid:id>/" , add_to_wishlist , name = "add-to-wishlist"),
    path("delete/<int:id>/" , delete_from_wishlist , name = "delete-from-wishlist"),
]