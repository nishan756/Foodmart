from .repository import BlogRepo
from django.core.paginator import Paginator

class BlogServie:

    repo = BlogRepo()

    def all_blogs(self , page:int , per_Page:int , query:dict):


        blogs = self.repo.all_blogs(query)

        paginator = Paginator(blogs , per_Page)

        blogs = paginator.get_page(page)

        return blogs

    def get_blog_detail(self , slug:str):
        return self.repo.get_blog_detail(slug)