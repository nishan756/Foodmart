from .repository import ShippingChargeRepo , ThanaRepo , DistrictRepo , BannerRepo

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

class BannerService:

    @staticmethod
    def get_active_banners():
        banners = BannerRepo.get_active_banners()
        heroes = []
        promoes = []
        
        for banner in banners:
            if banner.banner_type == "hero_banner":
                heroes.append(banner)
            else:
                promoes.append(banner)

        return {"heroes":heroes , "promoes":promoes[:2]}
    