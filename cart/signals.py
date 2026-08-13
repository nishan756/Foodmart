from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from cart.models import Cart
from django.dispatch import receiver

User = get_user_model()

@receiver(signal = post_save , sender = User)
def create_cart(sender , instance , created , **kwargs):

    if created:
        return Cart.objects.create(user = instance)