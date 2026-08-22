from .models import Product , ProductReview
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q , Prefetch , Count , Sum , Avg
from cart.models import OrderItem
from django.core.exceptions import MultipleObjectsReturned

class ProductRepo:

    def top_selling_products(self):
        products = OrderItem.objects.values("product").annotate(
            total_sold = Sum("qty"),
        ).order_by("-total_sold")

        return products

    def all_poroducts(self , query:dict):

        products = Product.objects.all()

        # Query
        title = query.get("title" , None)

        min_price = query.get("min_price" , None)

        max_price = query.get("max_price" , None)

        category = query.get("category" , None)

        order_by = query.get("order_by" , "-created_at")

        if title:
            products = products.filter(title__icontains = title)

        if min_price and max_price:
            products = products.filter(price__lte = min_price , price__gte = max_price)

        if category:
            products = products.filter(category__title__iexact = category)

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

class ProductReviewRepo:

    def get_user_review(self , product_id , user):
        return ProductReview.objects.filter(product__id = product_id , user = user).first()

    def add_review(self , user , product_id , rating:int , feedback:str):
        return ProductReview.objects.create(user = user , product_id = product_id , feedback = feedback , rating = rating)

    def delete_review(self , review_id , user):
        try:
            ProductReview.objects.get(id = review_id , user = user).delete()
        except Product.DoesNotExist:
            raise ObjectDoesNotExist()

class ProductRequestRepo:pass
