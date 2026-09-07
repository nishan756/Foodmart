from .models import ShippingCharge , Thana , District


class DistrictRepo:

    @staticmethod
    def get_districts():
        return District.objects.all()

class ThanaRepo:

    @staticmethod
    def get_thanas(district_id:int):
        return Thana.objects.filter(district__id = district_id).values("id" , "name")

class ShippingChargeRepo:

    @staticmethod
    def get_shipping_charge(thana_id:int):
        try:
            return ShippingCharge.objects.get(thana__id = thana_id)
        except ShippingCharge.DoesNotExist:
            return None

    