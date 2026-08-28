from django.utils.timezone import now
from .repository import CartItemRepo , CartRepo , OrderRepo
from uuid import UUID
from .models import Cart
from product.service import ProductService
from product.exceptions import OutOfStock
from django.core.paginator import Paginator
import urllib


class CartService:

    repo = CartRepo()

    def get_cart(self , user):
        return self.repo.get_cart(user)

class CartItemService:

    repo = CartItemRepo()

    def get_cartitem(self , id , cart):
        return self.repo.get_cartitem(id , cart)

    def get_cart_item_by_product_id(self , cart , id):
        return self.repo.get_cart_item_by_product_id(cart , id)

    def get_user_cart_items(self , cart:Cart):
        return self.repo.get_user_cart_items(cart)

    
    def add_item(self , id , cart , qty):
        product = ProductService().get_product(id)

        if product.stock <= 0:
            raise OutOfStock("This product is out of stock")

        elif product.stock < qty:
            raise ValueError("Qty must be equal or less than product")

        cart_item = self.get_cart_item_by_product_id(cart , id)

        if cart_item:
            return self.increase_qty(id = cart_item.id , cart = cart , qty = qty)

        return self.repo.add_item(product , cart , qty)

    def del_item(self , id:UUID , cart:Cart):
        return self.repo.del_item(self.get_cartitem(id , cart))

    def increase_qty(self , id:UUID , cart:Cart , qty:int):
        if qty <= 0:
            raise ValueError("Qty must be greater than 0")

        return self.repo.increase_qty(id , cart , qty)

    def decrease_qty(self , id:UUID , cart:Cart):
        return self.repo.decrease_qty(id , cart)

class OrderService:
    repo = OrderRepo()
    def get_user_orders(self , user , page , **query_param):

        orders = self.repo.get_user_orders(user , **query_param)

        paginator = Paginator(orders , 10)

        orders = paginator.get_page(page)

        return orders

    def get_order(self , id):
        return self.repo.get_order(id)

    
    def confirm_order(self , items , user , shipping_address , city , postal_code , phone_number , full_name , email ):
        return self.repo.confirm_order(items , user , shipping_address , city , postal_code , phone_number , full_name  , email)
