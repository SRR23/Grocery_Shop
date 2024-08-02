from django.shortcuts import render

# Create your views here.
import json, uuid
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckOutForm
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cart.carts import Cart, Coupon
from product.models import Product
from .models import OrderItem, Order
# Create your views here.


class CheckOut(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(self.request.POST)  # Pass request.POST for validation
        if form.is_valid():
            # data = form.cleaned_data
            # print(data)
            return JsonResponse({
                'success': True,
                'errors': None
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            })



# @method_decorator(csrf_exempt, name='dispatch')
class SaveOrder(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    
    def post(self, *args, **kwargs):
        customer_data = json.loads(self.request.body)
        cart = Cart(self.request)
        coupon_id = cart.coupon
        user_cart = Cart(self.request).cart
        products = Product.objects.filter(id__in=list(user_cart.keys()))
        ordered_products = []
        
        for product in products:
            order_item = OrderItem.objects.create(
                product = product,
                price = product.price,
                quantity = user_cart[str(product.id)]['quantity']
            )
            ordered_products.append(order_item)
            
        order = Order.objects.create(
            user = self.request.user,
            transaction_id = uuid.uuid4().hex,
            **customer_data
        )
        order.order_items.add(*ordered_products)
        
        if coupon_id:
            order.coupon = Coupon.objects.get(id = coupon_id)
            order.save()
        
        if float('%.2f' % cart.total()) != float(order.total_bill):
            order.paid = False
            order.save()
        
        cart.clear()
            
        return JsonResponse({'success': True})



class Orders(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)
    