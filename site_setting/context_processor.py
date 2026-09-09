from .models import SiteInfo , SocialLink

def get_site_info(request):

    site_info = SiteInfo.objects.first()

    return {"site_info":site_info}

def get_site_social_links(request):

    social_links = SocialLink.objects.all()

    return {"social_links":social_links}