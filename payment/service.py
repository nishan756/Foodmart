import stripe
from django.conf import settings
from django.urls import reverse
from .repository import PaymentRepo
from cart.models import Order
from core.exceptions import ObjectAlreadyExists

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:

    @staticmethod
    def create_payment(order:Order , transaction_id):
        if not PaymentService.check_order_payment_status(order.id):
            return PaymentRepo.create_payment(order , transaction_id)
        raise ObjectAlreadyExists("Payment already compledted for this order")

    @staticmethod
    def get_payment(user , order_id):
        return PaymentRepo.get_payment(user , order_id)

    @staticmethod
    def get_payment_by_session_id(user , stripe_session_id):
        return PaymentRepo.get_payment_by_session_id(user , stripe_session_id = stripe_session_id)
        
    

class StripeService:

    @staticmethod
    def create_checkout_session(request , order , payment):
        success_url = request.build_absolute_uri(
            reverse(
                "payment:success"
            )
        )

        cancel_url = request.build_absolute_uri(
            reverse(
                "payment:cancel"
            )
        )

        line_items = []

        for item in order.order_items.all():
            line_items.append({
                "price_data": {
                    "currency": "bdt",
                    "product_data": {
                        "name": item.product_title,
                    },
                    "unit_amount": int(item.total_price*100),
                },
                "quantity": item.qty,
            })

        session = stripe.checkout.Session.create(
            mode = "payment",
            line_items = line_items,
            shipping_options = [
                {
                    "shipping_rate_data":{
                        "type":"fixed_amount",
                        "fixed_amount":{
                            "currency":"bdt",
                            "amount": int(order.shipping_charge * 100),
                        },
                        "display_name": "Delivery Charge",
                    }
                }
            ],
            success_url = success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = cancel_url,
            metadata = {
                "order_id":str(order.id),
                "payment_id":str(payment.id),
                "transaction_id":str(payment.transaction_id),
            }
        )

        return session




    
