from django.db import models 
from django.core.exceptions import ValidationError

class District(models.Model):
    name = models.CharField(max_length = 100 , unique = True)

    def clean(self):
        qs = District.objects.filter(name__iexact=self.name)
        if self.pk:
            qs = qs.exclude(pk = self.pk)

        if qs.exists():
            raise ValidationError({'name': 'District with this name already exists.'})

    def __str__(self):
        return self.name

class Thana(models.Model):
    name = models.CharField(max_length = 100)
    district = models.ForeignKey(District, on_delete = models.CASCADE , related_name = "thanas")

    def __str__(self):
        return f"{self.district.name} : {self.name}"


class ShippingCharge(models.Model):
    thana = models.ForeignKey(Thana , on_delete = models.CASCADE)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default = True)
    created_at = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.thana.name}: {self.charge}"


class SiteInfo(models.Model):
    site_name = models.CharField(max_length = 100)

    site_logo = models.ImageField(upload_to = "site_logo/" , blank = True , null = True)

    site_favicon = models.ImageField(upload_to = "site_favicon/" , blank = True , null = True)

    location = models.CharField(max_length = 200 , blank = True , null = True)

    phone_number = models.CharField(max_length = 14 , unique = True)

    email = models.EmailField(unique = True)

    description = models.TextField(blank = True , null = True)

    def __str__(self):
        return self.site_name