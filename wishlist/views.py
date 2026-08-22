from django.shortcuts import render
from .service import WishlistService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required(login_url = "login")
@require_POST
def add_to_wishlist(request , product_id):pass

@login_required(login_url = "login")
@require_POST
def delete_from_wishlist(request , wishlist_id):pass
