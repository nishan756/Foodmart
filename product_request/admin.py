from django.contrib import admin
from .models import ProductRequest

@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ["product" , "user" , "status"]
    list_per_page = 100