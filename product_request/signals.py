from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ProductRequest
from core.services.email import EmailService
from threading import Thread

@receiver(signal = post_save , sender = ProductRequest)
def send_email(sender , instance , created , **kwargs):

    if created:
        subject = "Thanks for your interest"
        template_name = "email/request-created.html"

    elif instance.status == "cancelled":
        subject = "Your request has been cancelled"
        template_name = "email/request-cancelled.html"

    elif instance.status == "rejected":
        subject = "Your request has rejected"
        template_name = "email/request-rejected.html"
    
    kwargs = {
        "email_to":[instance.user.email],
        "subject":subject,
        "template_name":template_name,
        "context":{
            "user":instance.user,
            "product_url":f"localhost:8000/product/detail/{instance.product.id}/",
            "request":instance
        }
    }

    Thread(target = EmailService.send_email , kwargs = kwargs).start()