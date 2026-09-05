from django.shortcuts import render , redirect
from .service import StripeService , PaymentService
from cart.service import OrderService
from django.contrib import messages
import uuid
from django.core.exceptions import ObjectDoesNotExist
from core.exceptions import ObjectAlreadyExists
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from django.http import HttpResponse
from rest_framework import status
from .models import Payment
from django.views.decorators.http import require_GET

@login_required(login_url="login")
def start_payment(request, order_id):

    try:
        order = OrderService().get_order(order_id)

        if order.user != request.user:
            messages.warning(
                request,
                "You're not eligible to pay for this order"
            )
            return redirect("my-orders")

        payment = PaymentService.get_payment(
            request.user,
            order_id
        )

        if payment.status == Payment.StatusChoices.SUCCESS:
            messages.info(
                request,
                "Your payment is ok for this order"
            )
            return redirect("order-detail", order_id)

        transaction_id = f"TXN-{uuid.uuid4().hex[:20]}"

        payment.transaction_id = transaction_id

        session = StripeService.create_checkout_session(
            request,
            order,
            payment
        )

        payment.stripe_session_id = session.id

        payment.save(
            update_fields=[
                "stripe_session_id",
                "transaction_id"
            ]
        )

        return redirect(session.url)

    except ObjectDoesNotExist as e:
        messages.warning(request, str(e))

    except ObjectAlreadyExists as e:
        messages.info(request, str(e))

    except Exception:
        messages.error(request, "Something went wrong")

    return redirect("my-orders")

@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret = settings.STRIPE_WEBHOOK_SECRET,
        )

    except ValueError:
        return HttpResponse(status=400)

    except stripe.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        payment_id = session["metadata"]["payment_id"]

        payment = Payment.objects.filter(
            id=payment_id
        ).first()

        if payment and payment.status != Payment.StatusChoices.SUCCESS:

            payment.status = Payment.StatusChoices.SUCCESS

            payment.save(
                update_fields=["status"]
            )

    return HttpResponse(status=200)


@login_required(login_url="login")
@require_GET
def payment_success(request):

    stripe_session_id = request.GET.get("session_id")

    if not stripe_session_id:
        messages.info(request, "Payment not found")
        return redirect("my-orders")

    payment = PaymentService.get_payment_by_session_id(
        stripe_session_id=stripe_session_id,
        user = request.user
    )

    if not payment:
        messages.info(request, "Payment not found")
        return redirect("my-orders")

    return render(request , "payment-success.html", {"payment": payment})

@login_required(login_url = "login")
@require_GET
def payment_cancel(request):
    stripe_session_id = request.GET.get("session_id" , None)
    if not stripe_session_id:
        messages.info(request , "No payment found to cancel")
        return redirect("my-orders")
    return render(request , "payment-cancel.html")