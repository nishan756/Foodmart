from django.shortcuts import render , redirect
from .service import WishlistService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST , require_GET
from django.http import JsonResponse

from core.exceptions import ObjectAlreadyExists
from django.core.exceptions import ObjectDoesNotExist

from django.utils.http import url_has_allowed_host_and_scheme


@login_required(login_url = "login")
@require_GET
def my_wishlist(request):

    page = request.GET.get("page" , 1)

    # Query
    title = request.GET.get("title" , None)

    wishlist_items = WishlistService().get_user_wishlist_items(request.user , page , title)

    return render(request , "my-wishlist.html" , {"wishlist_items":wishlist_items})

@login_required(login_url = "login")
@require_POST
def add_to_wishlist(request , id):

    try:
        wishlist_item = WishlistService().add_to_wishlist(request.user , id)
        return JsonResponse({"message":"Successfully added {} in your wishlist".format(wishlist_item.product.title) , "tags":"success"})

    except ObjectAlreadyExists as e:
        return JsonResponse({"message":str(e) , "tags":"info"})

    except ObjectDoesNotExist as e:
        return JsonResponse({"message":str(e) , "tags":"info"})


@login_required(login_url = "login")
@require_POST
def delete_from_wishlist(request , id):
    try:
        WishlistService().delete_from_wishlist(request.user , id)
        return JsonResponse({"message":"Successfully removed wishlist item" , "tags":"success" , "status":200})
    
    except ObjectDoesNotExist as e:
        return JsonResponse({"message":str(e) , "tags":"info"})
    