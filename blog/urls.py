from .views import all_blogs , blog_detail
from django.urls import path

urlpatterns = [
    path('all/' , all_blogs , name = "all-blogs"),
    path('detail/<str:slug>/' , blog_detail , name = "blog-detail"),
]
