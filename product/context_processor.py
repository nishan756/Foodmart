from .models import ProductCategory
from django.db.models import Count , Q

def categories(request):
    categories = ProductCategory.objects.filter(is_active = True)\
    .annotate(total_item = Count("products" , distinct = True) + Count("sub_category__products"))
    return {"categories":categories}
