from .models import CartItem
from django.db.models.manager import BaseManager

def cart_detail(request):

    total_price = 0
    total_item = 0

    items:BaseManager[CartItem] = None

    if request.user.is_authenticated:
        items = CartItem.objects.filter(cart__user = request.user)

        total_price = 0

        total_item = 0

        for item in items:
            total_price += item.applicable_price()
            total_item += 1

    return {"total_price":total_price , "total_item":total_item , "items":items}
        
        
