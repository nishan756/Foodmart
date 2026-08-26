from .repository import ProductRepo , ProductReviewRepo
from django.core.paginator import Paginator
from .models import ProductReview
from core.exceptions import ObjectAlreadyExists
from django.core.exceptions import ObjectDoesNotExist


class ProductService:
    repo = ProductRepo()

    def all_products(self , page:int , per_page:int , query:dict):

        products =  self.repo.all_poroducts(query)

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