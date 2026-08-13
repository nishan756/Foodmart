from django.contrib import admin
from .models import ProductCategory , ProductBrand , Product , ProductImage , ProductReview
from django.utils.html import format_html

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["title" , "parent" , "is_active"]
    list_per_page = 100
    list_filter = ["is_active"]

@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["name" , "created_at" , "is_active"]
    list_per_page = 100
    list_filter = ["is_active"]

@admin.register(Product)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ["title" , "brand" , "price" , "discount" , "stock" , "is_active" , "is_featured"]
    list_per_page = 100
    list_filter = ["brand" , "is_active" , "is_featured"]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product" , "display_image"]
    list_per_page = 100

    def display_image(self , obj):
        return format_html(f"<img src={obj.image.url} height='30px;width='30px'>")

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user" , "product" , "rating" , "is_active" , "created_at" ]
    list_per_page = 100
    list_filter = ["is_active"]