from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator , MinValueValidator
from django_summernote.fields import SummernoteTextField
from django.contrib.auth import get_user_model
import uuid
from math import ceil

User = get_user_model()


class ProductBrand(models.Model):
    name = models.CharField(max_length = 50 , unique = True)

    logo = models.ImageField(upload_to = "product/brand_image")

    is_active = models.BooleanField(default = True)

    created_at = models.DateTimeField(default = now)

    def __str__(self):
        return self.name

    def clean(self):
        queryset  =ProductBrand.objects.filter(name__iexact = self.name)

        if self.pk:
            queryset = queryset.exclude(pk = self.pk)

        if queryset:
            raise ValidationError("This brand is already exists")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product Brand"
        verbose_name_plural = "Product Brands"

class ProductCategory(models.Model):
    title = models.CharField(max_length = 100)

    parent = models.ForeignKey("self" , blank = True , null = True , on_delete = models.SET_NULL , related_name = "sub_category")

    image = models.ImageField(blank = True , null = True , upload_to = "product/category_image")

    is_active = models.BooleanField(default = True)

    created_at = models.DateField(default = now)

    def __str__(self):
        return self.title

    def clean(self):
        queryset =  ProductCategory.objects.filter(title__iexact = self.title)

        if self.pk:
            queryset = queryset.exclude(pk = self.pk)

        if queryset:
            raise ValidationError(message = "Category with this title is already exists")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

class Product(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    title = models.CharField(max_length = 200)

    image = models.ImageField(upload_to = "product/image")

    brand = models.ForeignKey(ProductBrand , blank = True , null = True , on_delete = models.SET_NULL , related_name = "brand")

    category = models.ManyToManyField(ProductCategory , blank = True , related_name = "products")

    price = models.DecimalField(default = 0.0 , help_text = "in BDT" , decimal_places = 2 , max_digits = 8 , validators = [MinValueValidator(0.0 , "Product price can't less than 0")])

    discount = models.DecimalField(validators = [MaxValueValidator(100 , "Dsicount can't greater than 100") , MinValueValidator(0 , "Discount can't less than 0")] , default = 0.0 , decimal_places = 2 , max_digits = 5 , help_text = "In percentage")

    stock = models.PositiveIntegerField(default = 0)

    is_active = models.BooleanField(default = True)

    is_featured = models.BooleanField(default = False)

    description = SummernoteTextField(blank = True , null = True)

    created_at = models.DateTimeField(default = now)

    def __str__(self):
        return self.title

    @property
    def discount_price(self):

        price = self.price * self.discount / 100

        return price
    
    @property
    def applicable_price(self):

        price = self.price - self.discount_price

        return ceil(price)

    def save(self , *args , **kwargs):
        self.is_active = False if self.stock == 0 else True
        return super().save(*args , **kwargs)

    class Meta:
        ordering = ["-created_at"]

class ProductImage(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE , related_name = "images")

    image = models.ImageField(upload_to = "product/image")

    def __str__(self):
        return f"Image of {self.product.title}"

    class Meta:
        ordering = ["product"]


class ProductReview(models.Model):

    user = models.ForeignKey(User , on_delete = models.SET_NULL , blank = True , null = True)

    product = models.ForeignKey(Product , on_delete = models.CASCADE , related_name = "reviews")

    rating = models.PositiveIntegerField(
        validators = [
            MaxValueValidator(5 , message = "Rating can't greater than 5"),
        ],
        blank = True , null = True
    
    )

    feedback = models.TextField(blank = True , null = True)

    created_at = models.DateTimeField(default = now)

    is_active = models.BooleanField(default = False)

    class Meta:
        ordering = ["-created_at" , "rating"]
        unique_together = ["user" , "product"]
