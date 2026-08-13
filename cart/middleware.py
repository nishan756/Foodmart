from .models import Cart

class CartMiddleware:

    def __init__(self , get_response):
        self.get_response = get_response

    def __call__(self , request):
        if request.user.is_authenticated:
            cart , created = Cart.objects.get_or_create(user = request.user)

        else:
            
            if not request.session.session_key:
                request.session.create()

            session_id = request.session.session_key
            
            cart , created = Cart.objects.get_or_create(session_id = session_id)

        request.cart = cart
        
        response = self.get_response(request)

        return response


            