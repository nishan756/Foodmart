from django.contrib import admin
from .models import District, Thana, ShippingCharge


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Thana)
class ThanaAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    search_fields = ('district',)
    ordering = ["district"]

@admin.register(ShippingCharge)
class ShippingChargeAdmin(admin.ModelAdmin):
    list_display = ('thana', 'charge' , "is_active" , "created_at")