from .models import ProductRequest
from django.core.exceptions import ObjectDoesNotExist
from product.models import Product

class ProductRequestRepo:

    def check_user_request(self , user , product_id):
        return ProductRequest.objects.filter(user = user , product__id = product_id , status = "pending")

    def get_request(self , user , id):
        try:
            return ProductRequest.objects.get(id = id , user = user)
        except ProductRequest.DoesNotExist:
            raise ObjectDoesNotExist("Request not found")

    def create_request(self , user , product:Product , qty:int):
        return ProductRequest.objects.create(user = user , product = product , qty = qty)

    def get_requests(self , user):
        return ProductRequest.objects.filter(user = user)

    def cancel_request(self , user , id):
        request = self.get_request(user , id)
        request.status = "cancelled"
        return request.save()