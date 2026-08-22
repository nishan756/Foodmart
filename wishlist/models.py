from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Wishlist(models.Model):
    
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "wishlist")

    product = models.ForeignKey(Product , on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["product" , "user"]
