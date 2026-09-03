from .models import CartItem , Order , OrderItem , Cart
from product.models import Product
from product.service import ProductService
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from django.db import transaction
from product.exceptions import OutOfStock
from django.db.models import Count , Sum


class CartRepo:

    def get_cart(self , user):
        cart , created = Cart.objects.get_or_create(user = user)
        return cart


class CartItemRepo:

    def get_cartitem(self , id:UUID , cart:Cart)-> CartItem:
        try:
            return CartItem.objects.get(id = id , cart = cart)

        except CartItem.DoesNotExist:
            raise ObjectDoesNotExist('Item not found')

    def get_cart_item_by_product_id(self , cart , id):
        return CartItem.objects.filter(cart = cart , product__id = id).first()

    def get_user_cart_items(self , cart:Cart):
        return CartItem.objects.filter(cart = cart)

    def add_item(self , product:Product , cart:Cart , qty:int)->None:
        return CartItem.objects.create(
            cart = cart , 
            product = product,
            qty = qty,
        )
    
    def del_item(self , item:CartItem)->None:
        return item.delete()


    @transaction.atomic()
    def increase_qty(self , id:UUID , cart:Cart , qty:int)->None:

        try:
            cart_item = CartItem.objects.select_for_update().get(id = id , cart = cart)

        except CartItem.DoesNotExist:
            raise ObjectDoesNotExist("Cartitem not found")

        if cart_item.product.stock <= 0:
            raise OutOfStock("This product is out of stock")

        elif qty > cart_item.product.stock:
            raise ValueError("Qty must be less than or equal to stock")
        
        cart_item.qty += qty

        cart_item.save(update_fields = ["qty"])

        return

    @transaction.atomic()
    def decrease_qty(self , id:UUID , cart:Cart):

        try:
            cart_item = CartItem.objects.select_for_update().get(id = id , cart = cart)

        except CartItem.DoesNotExist:
            raise ObjectDoesNotExist("Cartitem not found")

        cart_item.qty -= 1

        deleted = False

        if cart_item.qty == 0:
            cart_item.delete()
            deleted = True
            return deleted
        
        cart_item.save(update_fields = ["qty"])

        return deleted

class OrderRepo:

    def get_user_orders(self , user , **query_param):

        date_from = query_param.get("date_from" , None)

        date_to = query_param.get("date_to" , None)

        orders = Order.objects.filter(user = user)

        if date_from and date_to:
            orders = orders.filter(created_at__date__gte = date_from , created_at__lte = date_to)
        elif date_from:
            orders = orders.filter(created_at__date__gte = date_from)
        elif date_to:
            orders = orders.filter(created_at__date__lte = date_to)

        orders = orders.annotate(total_item = Count("order_items"))

        return orders

    def get_order(self , id):
        try:
            return Order.objects.prefetch_related("order_items").get(id = id)
        except Order.DoesNotExist:
            raise ObjectDoesNotExist("Order not found")
        

    @transaction.atomic()
    def confirm_order(self , items , user , shipping_address , city , postal_code , phone_number , full_name , email):
        order = Order(user = user , full_name = full_name , email = email , phone_number = phone_number , shipping_address = shipping_address , city = city , postal_code = postal_code)

        canceled_item = []

        ordered_items = []

        total_price = 0

        for item in items:
            if item.product and item.qty <= item.product.stock:

                order_item = OrderItem.objects.create(user = user , product = item.product , order = order , product_title = item.product.title , product_image = item.product.image.url , unit_price = item.product.price , discount = item.product.discount , qty = item.qty , total_price = item.applicable_price())
                total_price += item.applicable_price()
                ordered_items.append(order_item)
                product = Product.objects.select_for_update().get(id = item.product.id)

                product.stock -= item.qty

                product.save(update_fields = ["stock"])

            else:
                canceled_item.append(item)

            CartItemRepo().del_item(item)

        if len(ordered_items) > 0:
            order.total_price = total_price
            order.save()

        return canceled_item
