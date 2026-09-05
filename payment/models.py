from django.db import models
from cart.models import Order

class Payment(models.Model):

    order = models.ForeignKey(Order , on_delete = models.CASCADE , related_name = "payment")

    transaction_id = models.CharField(max_length = 50 , unique = True , blank = True , null = True)

    stripe_session_id = models.CharField(max_length = 255 , unique = True , blank = True , null = True)

    amount = models.DecimalField(max_digits = 10 , decimal_places = 2)

    class StatusChoices(models.TextChoices):
        PENDING = "pending" , "Pending"
        SUCCESS = "success" , "Success"
        FAILED = "failed" , "Failed"
        CANCELLED = "cancelled" , "Cancelled"

    status = models.CharField(max_length = 10 , default = StatusChoices.PENDING , choices = StatusChoices.choices)

    created_at = models.DateTimeField(auto_now_add = True)
    
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["-created_at"]
