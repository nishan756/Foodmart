from .repository import WishlistRepo

from core.exceptions import ObjectAlreadyExists

from product.repository import ProductRepo

from django.core.paginator import Paginator


class WishlistService:

    repo = WishlistRepo()

    def get_user_wishlist_items(self , user , page:int , title:str):
        wishlist_items =  self.repo.get_user_wishlist_items(user , title)

        paginator = Paginator(wishlist_items , 20)

        wishlist_items = paginator.get_page(page)

        return wishlist_items

    def check_user_already_added_a_product_in_wishlist(self , user , id):
        return self.repo.check_user_already_added_a_product_in_wishlist(user , id)

    def add_to_wishlist(self , user , id):

        if self.check_user_already_added_a_product_in_wishlist(user , id):
            raise ObjectAlreadyExists("You already added this product in your wishlist")

        product = ProductRepo().get_product(id)

        return self.repo.add_to_wishlist(user , product)

    def delete_from_wishlist(self , user , id):

        return self.repo.delete_from_wishlist(user , id)
    