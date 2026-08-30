from django.contrib import admin
from .models import Blog , BlogTag

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title" , "created_at"]
    list_per_page = 100

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_per_page = 100