from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .service import CartItemService


@login_required(login_url = "login")
@require_POST
def add_item(request , id):

    try:
        qty = int(request.POST.get("qty" , 1))
        CartItemService().add_item(id , cart = request.cart , qty = qty)
        messages.success(request , "Successfully added to your cart")

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))
        return redirect("all-products")

    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("product-detail" , id)
    

@login_required(login_url = "login")
def del_item(request , id):
    pass

@login_required(login_url = "login")
def increase_qty(request , id):
    pass

@login_required(login_url = "login")
def decrease_qty(request , id):
    pass


