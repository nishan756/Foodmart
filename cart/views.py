from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST , require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from product.exceptions import OutOfStock
from .forms import OrderForm , OrderFilterForm
from .service import CartItemService , OrderService


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
@require_POST
def del_item(request , id):
    pass

@login_required(login_url = "login")
@require_POST
def increase_qty(request , id):
    try:
        CartItemService().increase_qty(id , request.cart , qty = 1)
        messages.success(request , "Successfully added to your cart")

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    except OutOfStock as e:
        messages.warning(request , "This product is out of stock")

    return redirect('checkout')

@login_required(login_url = "login")
@require_POST
def decrease_qty(request , id):
    try:
        deleted = CartItemService().decrease_qty(id , request.cart)
        messages.success(request , "Successfully decreased your product quantity" if not deleted else "Item removed from your cart")
    
    except ObjectDoesNotExist as e:
        messages.info(request , str(e))
    
    return redirect('checkout')



@login_required(login_url = "login")
@require_GET
def checkout(request):

    form = OrderForm(initial = {"full_name":request.user.get_full_name , "email":request.user.email})

    return render(request , "checkout.html" , {"form":form})

@login_required(login_url = "login")
@require_POST
def confirm_order(request):
    try:
        form = OrderForm(data = request.POST)

        if form.is_valid():

            full_name = form.cleaned_data.get("full_name" , request.user.get_full_name)

            email = form.cleaned_data.get("email" , request.user.email)

            phone_number = form.cleaned_data.get("phone_number")

            shipping_address = form.cleaned_data.get("shipping_address")

            city = form.cleaned_data.get("city")

            postal_code = form.cleaned_data.get("postal_code")

            items = CartItemService().get_user_cart_items(request.cart)

            canceled_items = OrderService().confirm_order(items , request.user , shipping_address , city , postal_code , phone_number , full_name , email)

            if canceled_items:
                messages.info(request , f"{[item.product.title for item in canceled_items]} these product has stocked out. We're sorry")
        else:
            messages.error(request , form.errors)

    except Exception as e:
        messages.error(request , "Something went wrong")

    return redirect("my-orders")

@login_required(login_url = "login")
@require_GET
def my_orders(request):
    form = OrderFilterForm(data = request.GET)

    query_param = {}

    if form.is_valid():
        query_param = form.cleaned_data

    page = request.GET.get("page" , 1)

    orders = OrderService().get_user_orders(request.user , page , **query_param)

    return render(request , "my-orders.html" , {"orders":orders , "form":form})

@require_GET
def order_detail(request , id):
    try:
        order = OrderService().get_order(id)
        return render(request , "order-detail.html" , {"order":order})
    
    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    return redirect("my-orders")