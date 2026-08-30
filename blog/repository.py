from .models import Blog
from django.core.exceptions import ObjectDoesNotExist

class BlogRepo:

    def all_blogs(self , query:dict):
        blogs = Blog.objects.all()

        if query.get("title"):
            blogs = blogs.filter(title__icontains = query.get("title"))

        return blogs

    def get_blog_detail(self , slug:str):
        try:
            return Blog.objects.prefetch_related("tags").get(slug = slug)

        except Blog.DoesNotExist:
            raise ObjectDoesNotExist("Blog not found")