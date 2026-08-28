from .models import Wishlist

from django.core.exceptions import ObjectDoesNotExist

class WishlistRepo:

    def get_user_wishlist_items(self , user , title):
        wishlist_items =  Wishlist.objects.filter(user = user)

        if title:
            wishlist_items = wishlist_items.filter(product__title__icontains = title)

        return wishlist_items


    def check_user_already_added_a_product_in_wishlist(self , user , id):
        return Wishlist.objects.filter(user = user , product__id = id).exists()

    def add_to_wishlist(self , user , product):

        return Wishlist.objects.create(user = user , product = product)

    def delete_from_wishlist(self , user , id):

        try:
            item = Wishlist.objects.get(user = user , id = id)
            item.delete()
            return

        except Wishlist.DoesNotExist:
            raise ObjectDoesNotExist("Wishlist item not found")