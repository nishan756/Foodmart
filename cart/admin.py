from django.contrib import admin
from .models import Cart , CartItem , OrderItem , Order
from django.contrib import messages


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
    actions = ["mark_selected_order_as_shipped" , "mark_selected_order_as_on_the_way" , "mark_selected_order_as_accepted" , "mark_selected_order_as_cancelled"]

    @admin.action(description = "Mark selected order as shipped")
    def mark_selected_order_as_shipped(self , request , queryset):
        try:
            shipped_order_count = queryset.update(status = "shipped")
            self.message_user(request , f"Successfully marked {shipped_order_count} order(s) as shipped" , messages.SUCCESS)

        except Exception as e:
            self.message_user(request = request , message = str(e) , level = messages.ERROR)

    @admin.action(description = "Mark selected order as on the way")
    def mark_selected_order_as_on_the_way(self , request , queryset):
        try:
            on_the_way_order_count = queryset.update(status = "on_the_way")
            self.message_user(request , f"Successfully marked {on_the_way_order_count} order(s) as on the way" , messages.SUCCESS)
            
        except Exception as e:
            self.message_user(request = request , message = str(e) , level = messages.ERROR)

    @admin.action(description = "Mark selected order as accepted")
    def mark_selected_order_as_accepted(self , request , queryset):

        try:
            accepted_order_count = queryset.update(status = "accepted")
            self.message_user(request , f"Successfully marked {accepted_order_count} order(s) as accepted" , messages.SUCCESS)

        except Exception as e:
            self.message_user(request = request , message = str(e) , level = messages.ERROR)


    @admin.action(description = "Mark selected order as cancelled")
    def mark_selected_order_as_cancelled(self , request , queryset):

        try:
            cancelled_count = queryset.update(status = "cancelled")
            self.message_user(request , f"Successfully marked {cancelled_count} order(s) as cancelled" , messages.SUCCESS)

        except Exception as e:
            self.message_user(request = request , message = str(e) , level = messages.ERROR)
