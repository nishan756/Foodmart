from django.dispatch import receiver
from django.db.models.signals import post_save
from cart.models import Order
from payment.models import Payment
from core.services.email import EmailService
from threading import Thread

@receiver(signal = post_save , sender = Order)
def create_initial_payment(sender , instance , created , **kwargs):
    if created:
        payment = Payment.objects.create(order = instance , amount = instance.total_price+instance.shipping_charge)


@receiver(signal = post_save , sender = Payment)
def send_mail(sender , instance , created , **kwargs):
    kwargs = {
        "email_to":[instance.order.user.email],
        "context":{
            "user":instance.order.user,
            "payment":instance

        }
    }

    if not created and instance.status == "success":
        kwargs["subject"] = "Your payment is successfull"
        kwargs["template_name"] = "payment-success.html"

        thread = Thread(target = EmailService.send_email , kwargs = kwargs)
        thread.start()



