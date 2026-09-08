from django.shortcuts import render , redirect

from django.contrib import messages

from .service import ProductService , ProductReviewService , ProductBrandService

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from .forms import ProductReviewForm

from django.views.decorators.http import require_GET , require_POST

from core.exceptions import ObjectAlreadyExists

from django.utils.http import url_has_allowed_host_and_scheme

from blog.service import BlogService

from django.http import JsonResponse

from site_setting.service import BannerService

def home(request):
    brands = ProductBrandService().all_brands()

    top_selling_products = ProductService().top_selling_products()

    newly_arrived_products = ProductService().newly_arrived_products()

    recent_blogs = BlogService().recent_blogs()

    banners = BannerService.get_active_banners()

    heroes = banners.pop("heroes")

    promoes = banners.pop("promoes")

    context = {"brands":brands , "top_selling_products":top_selling_products , "newly_arrived_products":newly_arrived_products , "recent_blogs":recent_blogs , "heroes":heroes , "promoes":promoes}
    return render(request , "home.html" , context)

def all_products(request):
    query = request.GET.dict()

    page = query.pop("page" , 1) 

    per_page = query.pop("per_page" , 100)

    try:page = int(page)
    except (ValueError , TypeError):page = 1

    try:per_page = int(per_page)
    except(ValueError , TypeError):per_page = 100

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

    try:
        ProductReviewService().delete_review(review_id = id , user = request.user)
        return JsonResponse({"message":"Successfully deleted your review" , "success":True , "tags":"success"})

    except ObjectDoesNotExist as e:
        return JsonResponse({"message":str(e) , "success":False , "tags":"info"})

    except Exception as e:
        return JsonResponse({"message":str(e) , "success":False , "tags":"warning"})