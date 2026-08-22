from .views import product_detail , all_products , product_request , product_review , delete_review

from django.urls import path


urlpatterns = [
    path("all/" , all_products , name = "all-products"),
    path("detail/<uuid:id>/" , product_detail , name = "product-detail"),

    path("request/<uuid:id>/" , product_request , name = "product-request"),
    path("post-review/<uuid:id>/" , product_review , name = "post-review"),
    path("delete-review/<int:id>/" , delete_review , name = "delete-review"),
]
