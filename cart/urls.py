from django.urls import path, include
from .views import *

urlpatterns = [
   path('cart_list/', Cart_Item.as_view(), name="cart_list"),
   path('add_cart/<int:product_id>/', Add_Cart.as_view(), name="add_cart"),
   path('add_coupon/', Add_Coupon.as_view(), name="add_coupon"),
]