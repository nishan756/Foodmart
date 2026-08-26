from django.shortcuts import render , redirect

from django.contrib import messages

from .service import ProductService , ProductReviewService

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from .forms import ProductReviewForm

from django.views.decorators.http import require_GET , require_POST

from core.exceptions import ObjectAlreadyExists

from django.utils.http import url_has_allowed_host_and_scheme

def home(request):
    return render(request , "home.html")

def all_products(request):
    query = request.GET.dict()

    page = query.pop("page" , 1)

    per_page = query.pop("per_page" , 100)

    products = ProductService().all_products(page , per_page , query)

    return render(request , "all-products.html" , {"products":products})

@require_GET
def product_detail(request , id):

    try:
        product = ProductService().product_detail(id)
        return render(request , "product-detail.html" , {"product":product , "form":ProductReviewForm()})

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    return redirect("home")

@login_required(login_url = "login")
@require_POST
def product_review(request , id):
    form = ProductReviewForm(data = request.POST)
    if form.is_valid():
        user = request.user
        product_id = id
        rating = form.cleaned_data.get("rating")
        feedback = form.cleaned_data.get("feedback")
        try:
            ProductReviewService().add_review(user , product_id , rating , feedback)
            messages.success(request , "Thanks for your review")

        except ObjectAlreadyExists as e:
            messages.info(request , str(e))

        except Exception as e:
            messages.error(request , "Something went wrong")

    messages.error(request , str(form.errors))
    return redirect("product-detail" , id)

@login_required(login_url = "login")
@require_POST
def delete_review(request , id):

    HTTP_REFERER = request.META.get("HTTP_REFERER")

    try:
        ProductReviewService().delete_review(review_id = id , user = request.user)

    except ObjectDoesNotExist as e:
        messages.info(request , str(e))

    except Exception as e:
        print(e)
        messages.error(request , "Something went wrong")

    return redirect(HTTP_REFERER if url_has_allowed_host_and_scheme(HTTP_REFERER , request.get_host()) else "home")