from .models import SiteInfo

def get_site_info(request):

    site_info = SiteInfo.objects.first()

    return {"site_info":site_info}