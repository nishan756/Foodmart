from .models import Product , ProductReview , ProductBrand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q , Prefetch , Count , Sum , Avg
from cart.models import OrderItem
from datetime import timedelta , datetime


class ProductBrandRepo:

    def all_brands(self):
        return ProductBrand.objects.filter(is_active = True).order_by("-created_at")
    
class ProductRepo:

    def top_selling_products(self):
        products = OrderItem.objects.prefetch_related("product__reviews")\
            .values("product" , "product__id" , "product__title" , "product__discount" , "product__price" , "product__image")\
            .annotate(
                total_sold = Sum("qty"),
                avg_review = Avg("product__reviews__rating" , default = 0.0)
            )\
            .order_by("-total_sold")
        
        return products

    def newly_arrived_products(self):
        today = datetime.today().date()

        last_7_days = today - timedelta(days = 7)

        products = Product.objects.filter(created_at__date__gte = last_7_days).annotate(avg_review = Avg("reviews__rating" , default = 0))

        return products.order_by("-created_at")

    def all_products(self , query:dict):

        products = Product.objects.all()

        # Query
        title = query.get("title" , None)

        min_price = query.get("min_price" , None)

        max_price = query.get("max_price" , None)

        category = query.get("category" , None)

        brand = query.get("brand" , None)
        

        order_by = query.get("order_by" , "-created_at")

        if title:
            products = products.filter(title__icontains = title)

        if min_price and max_price:
            products = products.filter(price__gte = min_price , price__lte = max_price)

        elif min_price:
            products = products.filter(price__gte = min_price)

        elif max_price:
            products = products.filter(price__lte = max_price)

        if category:
            products = products.filter(category__title__iexact = category)

        if brand:
            products = products.filter(brand__name__iexact = brand)

        products = products.annotate(avg_rating = Avg("reviews__rating"))

        return products.order_by(order_by)

    def get_product(self , id):
        try:
            return Product.objects.get(id = id)

        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Product not found")

    def product_detail(self , id):
        try:
            return Product.objects\
                .select_related("brand")\
                .prefetch_related("images" , "category" , "reviews")\
                .annotate(total_review = Count("reviews") , avg_review = Avg("reviews__rating" , distinct = True))\
                .get(id = id)
        
        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Product not found")

    def decrease_stock(self , qty:int):
        try:
            product = Product.objects.select_for_update().get(id = id)

            product.stock -= qty

            product.save(update_fields = ["stock"])

        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Product not found")

class ProductReviewRepo:

    def get_user_review(self , product_id , user):
        return ProductReview.objects.filter(product__id = product_id , user = user).first()

    def add_review(self , user , product_id , rating:int , feedback:str):
        return ProductReview.objects.create(user = user , product_id = product_id , feedback = feedback , rating = rating)

    def delete_review(self , review_id , user):
        try:
            ProductReview.objects.get(id = review_id , user = user).delete()
        except Product.DoesNotExist:
            raise ObjectDoesNotExist("Review not found")
