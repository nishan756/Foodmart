from .views import start_payment , payment_cancel , payment_success , stripe_webhook
from django.urls import path

app_name = "payment"

urlpatterns = [
    path("start/<str:order_id>/" , start_payment , name = "start-payment"),
    path("success/" , payment_success , name = "success"),
    path("cancel/" , payment_cancel , name = "cancel"),
    path("webhook/", stripe_webhook, name="webhook"),
]
