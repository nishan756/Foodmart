from django.db import models
from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError
import uuid
from product.models import Product
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.timezone import now


User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , blank = True , null = True)

    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Cart of {self.user}"

    class Meta:
        ordering = ["-created_at"]  

class CartItem(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    cart = models.ForeignKey(Cart , on_delete = models.CASCADE , related_name = "items")

    product = models.ForeignKey(Product , on_delete = models.CASCADE , related_name = "cart_items")

    qty = models.PositiveIntegerField(validators = [MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add = True)

    def applicable_price(self):
        return self.product.applicable_price * self.qty

    class Meta:
        ordering = ["-created_at"]

class OrderItem(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    user = models.ForeignKey(User , on_delete = models.SET_NULL , blank = True , null = True)

    product = models.ForeignKey(Product , on_delete = models.SET_NULL , blank = True , null = True , related_name = "order_items")

    order = models.ForeignKey("Order" , on_delete = models.PROTECT , blank = True , null = True , related_name = "order_items")

    product_title = models.CharField(max_length = 200)

    product_image = models.URLField(blank = True , null = True)

    unit_price = models.DecimalField(default = Decimal("0.00") , decimal_places = 2 , max_digits = 8)

    discount = models.DecimalField(default = Decimal("0.00") , decimal_places = 2 , max_digits = 5)

    qty = models.PositiveIntegerField(validators = [MinValueValidator(1)])

    total_price = models.DecimalField(default = Decimal("0.00") , decimal_places = 2 , max_digits = 8)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created_at"]


class Order(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    user = models.ForeignKey(User , on_delete = models.SET_NULL , blank = True , null = True)

    # User info snapshot
    full_name = models.CharField(max_length = 100)

    email = models.EmailField(blank = True , null = True)

    phone_number = models.CharField(max_length = 14)

    # Shipping 
    shipping_address = models.CharField(max_length = 200)

    city = models.CharField(max_length = 100)

    postal_code = models.CharField(max_length = 20)

    total_price = models.DecimalField(max_digits = 8 , decimal_places = 2 , default = Decimal("0.00"))

    shipping_charge = models.PositiveIntegerField(default = 50)

    
    class PaymentTypeChoices(models.TextChoices):
        COD = "cod" , "Cash On Delivery"
        ONLINE_PAYMENT = "online_payment" , "Online Payment"

    payment_type = models.CharField(max_length = 15 , default = PaymentTypeChoices.COD , choices = PaymentTypeChoices.choices)

    class OrderStatus(models.TextChoices):
        PENDING = "pending" , "Pending"

        ACCEPTED = "accepted" , "Accepted"

        ON_THE_WAY = "on_the_way" , "On the way"

        CANCELLED = "cancelled" , "Cancelled"

        SHIPPED = "shipped" , "Shipped"

    status = models.CharField(max_length = 20 , choices = OrderStatus.choices , default = OrderStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add = True)

    shipped_at = models.DateTimeField(blank = True , null = True)

    def __str__(self):
        return  f"Order of {self.user.get_full_name}"

    @property
    def get_order_id(self):
        _id = f"{str(self.id).split("-")[0]}-{self.created_at.date()}-{self.user.username}"
        return _id

    def save(self , *args , **kwargs):

        if self.status == "shipped" and self.shipped_at is None:

            self.shipped_at = now()

        super().save(*args , **kwargs)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields = ["-created_at"]),
            models.Index(fields = ["user" , "-created_at"]),
            models.Index(fields = ["status" , "-created_at"]),
            models.Index(fields = ["phone_number"]),
            models.Index(fields = ["email"])
        ]