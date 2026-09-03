from django.urls import path
from .views import all_requests , create_request , cancel_request , product_request_detail

urlpatterns = [
    path('' , all_requests , name = 'all-requests'),
    path("detail/<int:id>" , product_request_detail , name = 'product-request-detail'),

    path("create/<uuid:product_id>" , create_request , name = 'create-request'),
    path("cancel/<int:id>" , cancel_request , name = 'cancel-request'),

]
