from typing import Any
from datetime import datetime
from django.utils import timezone
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .carts import Cart
from product.models import Product
from .models import Coupon
from django.contrib import messages
# Create your views here.


class Add_Cart(generic.View):
    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id, 1)
        
        return redirect('cart_list')



class Cart_Item(generic.TemplateView):
    template_name = 'cart.html'
    
    # This is for quantity increase and decrease
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id', None)
        quantity = request.GET.get('quantity', None)
        clear = request.GET.get('clear', False)
        cart = Cart(request)
        
        
        if product_id and quantity:
            product = get_object_or_404(Product, id=product_id)
            
            if int(quantity) > 0:
                if product.in_stock:
                    cart.update(int(product_id), int(quantity))
                    return redirect('cart_list')
                else:
                    return redirect('cart_list')
            else:
                cart.update(int(product_id), int(quantity))
                return redirect('cart_list')
            
        
        if clear:
            cart.clear()
            return redirect('cart_list')
        
        return super().get(request, *args, **kwargs)



class Add_Coupon(generic.View):
    def post(self, *args, **kwargs):
        code = self.request.POST.get('coupon', '')
        coupon = Coupon.objects.filter(code__iexact=code, active=True)
        cart = Cart(self.request)
        
        if coupon.exists():
            coupon = coupon.first()
            current_date = datetime.date(timezone.now())
            active_date = coupon.active_date
            expiry_date = coupon.expiry_date
            
            if current_date > expiry_date:
                messages.warning(self.request, "Coupon Expired")
                return redirect('cart_list')
            
            if current_date < active_date:
                messages.warning(self.request, "Coupon is available soon")
                return redirect('cart_list')
            
            if cart.total() < coupon.miniAmountToUseCoupon:
                messages.warning(self.request, f"You have to buy minimum ${coupon.miniAmountToUseCoupon} to avail coupon")
                return redirect('cart_list')
            
            cart.add_coupon(coupon.id)
            messages.success(self.request, "Coupon added successfully")
            return redirect('cart_list')
        
        else:
            messages.warning(self.request, "Invalid Coupon Code")
            return redirect('cart_list')