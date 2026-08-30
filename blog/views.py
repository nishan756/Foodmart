from django.shortcuts import render , redirect
from .service import BlogService
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

@require_GET
def all_blogs(request):

    query = request.GET.dict()

    page = query.pop("page" , 1)

    per_page = query.pop("per_page" , 100)

    try:page = int(page)
    except(ValueError , TypeError):page = 1

    try:per_page = int(per_page)
    except(ValueError , TypeError):per_page = 100

    try:blogs = BlogService().all_blogs(page , per_page , query);return render(request , "all-blogs.html" , {"blogs":blogs})
    except Exception:messages.error(request , "Something went wrong in this page. Try again later")

    return redirect("all-products")

@require_GET
def blog_detail(request , slug):

    
    try:blog = BlogService().get_blog_detail(slug);return render(request , "blog-detail.html" , {"blog":blog})
    except ObjectDoesNotExist as e:messages.info(request , str(e))

    return redirect("all-blogs")