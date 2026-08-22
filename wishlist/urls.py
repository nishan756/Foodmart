from django.urls import path
from .views import add_to_wishlist , delete_from_wishlist

urlpatterns = [
    path("add/<uuid:product_id>/" , add_to_wishlist , name = "add-to-wishlist"),
    path("delete/<int:wishlist_id>/" , delete_from_wishlist , name = "delete-from-wishlist"),
]