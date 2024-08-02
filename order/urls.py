
from django.urls import path
from .views import *
urlpatterns = [
    
    path('checkout/', CheckOut.as_view(), name="checkout"),
    path('save_order/', SaveOrder.as_view(), name="save_order"),
    path('orders/', Orders.as_view(), name="orders"),
]