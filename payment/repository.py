from .models import Payment
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Order

class PaymentRepo:

    @staticmethod
    def get_payment(user , order_id):

        try:
            return Payment.objects.get(order_id = order_id , order__user = user)

        except Payment.DoesNotExist:
            raise ObjectDoesNotExist("Payment info not found")

    @staticmethod
    def get_payment_by_session_id(user , stripe_session_id):
        try:
            return Payment.objects.get(order__user = user , stripe_session_id = stripe_session_id)
        except Payment.DoesNotExist:
            raise ObjectDoesNotExist("Payment not found")

    @staticmethod
    def create_payment(order:Order , transaction_id):
        return Payment.objects.create(
            order = order,
            transaction_id = transaction_id,
            amount = order.total_price+order.shipping_charge,

        )
