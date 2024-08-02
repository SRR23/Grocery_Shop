from .carts import Cart
from .models import Coupon

def cart(request):
    cart = Cart(request)
    
    if len(list(cart.cart.keys())) < 1:
        try:
            del cart.session[cart.coupon_id]
        except:
            pass
        
    return {"cart": Cart(request)}


def coupon_codes(request):
    coupons = Coupon.objects.filter(active=True)
    return {'coupon_codes': coupons}