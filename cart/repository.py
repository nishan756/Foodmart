from .models import CartItem , Order , OrderItem , Cart
from product.models import Product
from product.service import ProductService
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from django.db import transaction
from core.exceptions import OutOfStock


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

    def add_item(self , product:Product , cart:Cart , qty:int)->None:
        return CartItem.objects.create(
            cart = cart , 
            product = product,
            qty = qty,
        )
    
    def del_item(self , item:CartItem)->None:
        return item.delete()


    @transaction.atomic()
    def increase_qty(self , id:UUID , qty:int)->None:

        try:
            cart_item = CartItem.objects.select_for_update().get(id = id)

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
    def decrease_qty(self , id:UUID , qty:int)->None:

        try:
            cart_item = CartItem.objects.select_for_update().get(id = id)

        except CartItem.DoesNotExist:
            raise ObjectDoesNotExist("Cartitem not found")

        if cart_item.product.stock <= 0:
            raise OutOfStock("This product is out of stock")

        if cart_item.product.stock < qty:
            raise ValueError("Qty must be less than or equal to stock")
        

        cart_item.qty -= qty

        if cart_item.qty == 0:
            return cart_item.delete()

        cart_item.save(update_fields = ["qty"])

        return 
