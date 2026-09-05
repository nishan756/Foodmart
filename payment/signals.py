from django.dispatch import receiver
from django.db.models.signals import post_save
from cart.models import Order
from payment.models import Payment
from core.services.email import EmailService

@receiver(signal = post_save , sender = Order)
def create_initial_payment(sender , instance , created , **kwargs):
    if created:
        payment = Payment.objects.create(order = instance , amount = instance.total_price+instance.shipping_charge)

    elif instance.status == "success":
        kwargs = {

        }

        

