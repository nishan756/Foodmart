from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from cart.models import Cart , Order
from django.dispatch import receiver
from threading import Thread
from core.services.email import EmailService

User = get_user_model()

@receiver(signal = post_save , sender = User)
def create_cart(sender , instance , created , **kwargs):

    if created:
        return Cart.objects.create(user = instance)


@receiver(signal = post_save , sender = Order)
def send_email(sender , instance , created , **kwargs):

    kwargs = {
        "email_to":[instance.user.email],
        "context":{
            "instance":instance,
            "user":instance.user,
        }
    }

    if created:
        kwargs["subject"] = "Thanks for your order."
        kwargs["template_name"] = "email/order-completed.html"

    else:
        if instance.status == "shipped":
            kwargs["subject"] = "Your order has reached."
            kwargs["template_name"] = "email/order-shipped.html"

    thread = Thread(target = EmailService.send_email , kwargs = kwargs)

    thread.start()