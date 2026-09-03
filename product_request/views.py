from django.shortcuts import render , redirect
from .service import ProductRequestService
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from core.exceptions import ObjectAlreadyExists
from django.contrib import messages



@login_required(login_url = "login")
@require_GET
def all_requests(request):
    # Fetching page number
    page = request.GET.get("page" , 1)

    # Handling exception
    try:page = int(page)
    except(ValueError , TypeError):page = 1

    # Fetching product requests
    requests = ProductRequestService().get_requests(request.user , page)

    return render(request , "all-requests.html" , {"requests":requests})


@login_required(login_url = "login")
@require_POST
def create_request(request , product_id):
    qty = request.POST.get("qty" , 1)
    try:qty = int(qty)
    except(ValueError , TypeError):qty = 1

    try:
        product_request = ProductRequestService().create_request(request.user , product_id , qty)
        messages.success(request , f"Successfully create request for {product_request.product.title}")
        return redirect("all-requests")

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    except ObjectAlreadyExists as e:
        messages.info(request , str(e))

    return redirect("product-detail" , product_id)


def product_request_detail(request , id):
    try:
        product_request = ProductRequestService().get_request(request.user , id)
        return render(request , "request-detail.html" , {"product_request":product_request})

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("all-requests")

@login_required(login_url = "login")
@require_POST
def cancel_request(request , id):
    try:
        ProductRequestService().cancel_request(request.user , id)

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("all-requests")