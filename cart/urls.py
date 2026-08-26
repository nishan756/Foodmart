from django.urls import path
from .views import add_item , del_item , increase_qty , decrease_qty , checkout , confirm_order , my_orders , order_detail


urlpatterns = [
    path("add/<uuid:id>/" , add_item , name = "add-item"),
    path("delete/<uuid:id>/" , del_item , name = "del-item"),
    path("increase-qty/<uuid:id>/" , increase_qty , name = "increase-qty"),
    path("decrease-qty/<uuid:id>/" , decrease_qty , name = "decrease-qty"),
    path("checkout/" , checkout , name = "checkout"),
    path("confirm-order/" , confirm_order , name = "confirm-order"),
    path("my-orders/" , my_orders , name = "my-orders"),
    path("order-detail/<uuid:id>/" , order_detail , name = "order-detail"),
]
