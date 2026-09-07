from django.shortcuts import render
from .service import ShippingChargeService , ThanaService
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def get_thana_list(request):
    district_id = request.GET.get("district_id")

    if not district_id:
        return JsonResponse(data = {"success":False , "message":"District is required"} , status = 400)
    
    thanas = list(ThanaService.get_thanas(district_id))
    
    return JsonResponse(data = {"thanas":thanas , "success":True})

@csrf_exempt
def get_shipping_charge(request):
    thana_id = request.GET.get("thana_id")

    if not thana_id:
        return JsonResponse(data = {"success":False , "message":"You must provide thana"})

    shipping_charge = ShippingChargeService.get_shipping_charge(thana_id)

    return JsonResponse(data = {"success":True , "charge":shipping_charge.charge if shipping_charge else "None"})
