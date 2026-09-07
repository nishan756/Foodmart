from .views import get_thana_list , get_shipping_charge
from django.urls import path

urlpatterns = [
    path('thana-list/' , get_thana_list , name = "thana-list"),
    path('shipping-charge/' , get_shipping_charge , name = "shipping-charge"),
]
