from django.contrib import admin
from .models import Cart , CartItem , OrderItem , Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user" , "created_at"]
    list_per_page = 100


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart" , "product" , "qty" , "applicable_price"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product" , "unit_price" , "order" , "created_at"]
    list_per_page = 100

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["get_order_id" , "user" , "total_price" , "status" , "created_at" , "shipped_at"]
    list_per_page = 100
