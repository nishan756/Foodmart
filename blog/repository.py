from .models import Blog
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta , datetime

class BlogRepo:

    def all_blogs(self , query:dict):
        blogs = Blog.objects.all()

        if query.get("title"):
            blogs = blogs.filter(title__icontains = query.get("title"))

        return blogs

    def recent_blogs(self):

        today = datetime.today().date()

        last_7_days = today - timedelta(days = 7)

        blogs = Blog.objects.filter(created_at__gte = last_7_days)

        return blogs.order_by("-created_at")

    def get_blog_detail(self , slug:str):
        try:
            return Blog.objects.prefetch_related("tags").get(slug = slug)

        except Blog.DoesNotExist:
            raise ObjectDoesNotExist("Blog not found")