from django.contrib import admin
from .models import District, Thana, ShippingCharge , SiteInfo , Banner , SocialLink


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

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone_number')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["banner_type" , "is_active" , "expires_at" , "created_at"]
    
    actions = ["mark_selected_banner_as_inactive" , "mark_selected_banner_as_active"]

    @admin.action(description = "Mark selected banner as inactive")
    def mark_selected_banner_as_inactive(self , request , queryset):
        banner_count = queryset.update(is_active = False)
        self.message_user(request , "Successfully marked {} banner as inactive".format(banner_count))

    @admin.action(description = "Mark selected banner as active")
    def mark_selected_banner_as_active(self , request , queryset):
        banner_count = queryset.update(is_active = True)
        self.message_user(request , "Successfully marked {} banner as active".format(banner_count))

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ["name" , "url"]