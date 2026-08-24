from django.utils.timezone import now
from .repository import CartItemRepo , CartRepo
from uuid import UUID
from .models import Cart
from product.service import ProductService
from product.exceptions import OutOfStock


class CartService:

    repo = CartRepo()

    def get_cart(self , user):
        return self.repo.get_cart(user)

class CartItemService:

    repo = CartItemRepo()

    def get_cartitem_by_cart_id(self , id , cart):
        return self.repo.get_cartitem(id , cart)

    def get_cart_item_by_product_id(self , cart , id):
        return self.repo.get_cart_item_by_product_id(cart , id)

    
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
