from .repository import ShippingChargeRepo , ThanaRepo , DistrictRepo

class DistrictService:

    @staticmethod
    def get_districts():
        return DistrictRepo.get_districts()


class ThanaService:

    @staticmethod
    def get_thanas(district_id:int):
        return ThanaRepo.get_thanas(district_id)


class ShippingChargeService:

    @staticmethod
    def get_shipping_charge(tahana_id:int):
        return ShippingChargeRepo.get_shipping_charge(tahana_id)