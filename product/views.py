from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator, InvalidPage
from django.db.models import Q
from .models import *
from .forms import ReviewForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

class Custom_Paginator:
    def __init__(self, request, queryset, paginated_by):
        self.paginator = Paginator(queryset, paginated_by)
        self.paginated_by = paginated_by
        self.queryset = queryset
        self.page = request.GET.get('page', 1)
        
    def get_queryset(self):
        try:
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)
        
        return queryset
    

class Home(generic.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                
                'featured_categories': Category.objects.filter(featured=True),
                'best_selling': Product.objects.filter(is_bestSelling=True),
                'banners': Banner.objects.filter(featured=True),
                'reviews': Review.objects.all(),
                
            }
        )
        
        vegetables = Category.objects.get(title='Vegetables')
        fruits = Category.objects.get(title='Fruits')
        
        context['current_path'] = self.request.path
        context['all_vegetables'] = Product.objects.filter(category=vegetables)
        context['all_fruits'] = Product.objects.filter(category=fruits)
        
        return context


class Product_details(generic.DetailView):
    model = Product
    template_name = 'shop-detail.html'
    context_object_name = 'P'
    slug_url_kwarg = 'slug'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        context['review_form'] = ReviewForm()
        context['average_rating'] = self.get_object().get_average_rating()
        
        return context


@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect(reverse('product_details', args=[product.slug]))
    else:
        form = ReviewForm()
    return render(request, 'shop-detail.html', {'P': product, 'review_form': form})


    
# class BestSelling_details(generic.DetailView):
#     model = BestSellingProduct
#     template_name = 'bestSelling_details.html'
#     context_object_name = 'P'
#     slug_url_kwarg = 'slug'
    
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['related_products'] = self.get_object().related
        
#         return context


class Product_Lists(generic.ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'product_lists'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = Custom_Paginator(self.request, self.get_queryset(), self.paginate_by)
        queryset = page_obj.get_queryset()
        paginator = page_obj.paginator
        context['product_list'] = queryset
        context['paginator'] = paginator
        context['current_path'] = self.request.path
        
        return context



class Category_details(generic.DetailView):
    model = Category
    template_name = 'category_details.html'
    slug_url_kwarg = 'slug'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = self.get_object()
        category_products = category.products.all()
        
        page_obj = Custom_Paginator(self.request, category_products, self.paginate_by)
        queryset = page_obj.get_queryset()
        
        context['product_list'] = queryset
        context['paginator'] = page_obj.paginator
        context['page_obj'] = queryset
        context['is_paginated'] = queryset.has_other_pages()
        
        return context




class Search_Products(generic.View):

    def get(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        products = Product.objects.filter(
            Q(title__icontains=key) |
            Q(category__title__icontains=key)
        )

        context = {
            'product_list': products,
            'key': key
        }

        return render(self.request, 'search_products.html', context)



