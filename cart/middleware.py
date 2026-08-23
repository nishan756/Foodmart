from .service import CartService

class CartMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.cart = None

        if request.user.is_authenticated:
            request.cart = CartService().get_cart(
                user=request.user
            )

        response = self.get_response(request)

        return response
