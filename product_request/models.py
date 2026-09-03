from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator

User = get_user_model()

class ProductRequest(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "product_requests")

    product = models.ForeignKey(Product , on_delete = models.CASCADE  , related_name = "product_requests")

    qty = models.PositiveIntegerField(default = 1 , validators = [MinValueValidator(1 , "Quantity must be at least 1") , MaxValueValidator(10 , "Quantity can't exceed 10")])

    class RequestStatus(models.TextChoices):
        PENDING = "pending" , "Pending"
        APPROVED = "approved" , "Approved"
        REJECTED = "rejected" , "Rejected"
        CANCELLED = 'cancelled' , "Cancelled"

    status = models.CharField(max_length = 10 , choices = RequestStatus.choices , default = RequestStatus.PENDING)

    admin_note = models.TextField(blank = True , null = True)
    
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user" , "product" , "status"]
