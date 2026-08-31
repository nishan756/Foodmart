from .repository import ProductRepo , ProductReviewRepo , ProductBrandRepo
from django.core.paginator import Paginator
from .models import ProductReview
from core.exceptions import ObjectAlreadyExists

class ProductBrandService:
    repo = ProductBrandRepo()

    def all_brands(self):
        return self.repo.all_brands()


class ProductService:
    repo = ProductRepo()

    def top_selling_products(self):
        return self.repo.top_selling_products()

    def newly_arrived_products(self):
        return self.repo.newly_arrived_products()

    def all_products(self , page:int , per_page:int , query:dict):

        supported_query_param = {"order_by" , "min_price" , "max_price" , "title" , "category" , "brand"}

        supported_ordering_param = {"price_low_to_high" , "price_high_to_low" , "old_to_new" , "new_to_old" , "rating_high_to_low" , "rating_low_to_high"}

        query = {key:value for key , value in query.items() if key in supported_query_param}

        if query.get("order_by"):
            query["order_by"] = query["order_by"] if query["order_by"] in supported_ordering_param else query.pop("order_by")

        products =  self.repo.all_products(query)

        paginator = Paginator(products , per_page)

        products = paginator.get_page(page)

        return products

    def get_product(self , id):
        return self.repo.get_product(id)

    def product_detail(self , id):
        return self.repo.product_detail(id)


class ProductReviewService:

    repo = ProductReviewRepo()

    def get_user_review(self , product_id , user):
        return self.repo.get_user_review(product_id , user)

    def add_review(self , user , product_id , rating , feedback):

        if self.get_user_review(product_id = product_id , user = user):
            raise ObjectAlreadyExists("You've already gave review on this product")
    
        return self.repo.add_review(user , product_id , rating , feedback)

    def delete_review(self , review_id , user):
        return self.repo.delete_review(review_id , user)