from .repository import ProductRequestRepo
from product.service import ProductService
from core.exceptions import ObjectAlreadyExists
from django.core.paginator import Paginator

class ProductRequestService:

    repo = ProductRequestRepo()

    def check_user_request(self , user , product_id):
        return self.repo.check_user_request(user , product_id)
    
    def get_request(self , user , id):
        return self.repo.get_request(user , id)
    
    def create_request(self , user , product_id , qty:int):
        if self.check_user_request(user , product_id):
            raise ObjectAlreadyExists("You already make request for this product")
        
        if qty < 1:
            raise ValueError("Qty must be at least 1")
        
        product = ProductService().get_product(product_id)
        return self.repo.create_request(user , product , qty)
    
    def get_requests(self , user , page:int):
        product_requests = self.repo.get_requests(user)
        
        paginator = Paginator(product_requests , 20)
        
        product_requests = paginator.get_page(page)

        return product_requests
    
    def cancel_request(self , user , id):
        return self.repo.cancel_request(user , id)