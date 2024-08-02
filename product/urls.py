from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('product_details/<str:slug>/', Product_details.as_view(), name="product_details"),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
    # path('best_details/<str:slug>/', BestSelling_details.as_view(), name="best_details"),
    path('product_list/', Product_Lists.as_view(), name="product_list"),
    path('category_details/<str:slug>/', Category_details.as_view(), name="category_details"),
    path('search_products/', Search_Products.as_view(), name="search_products"),
    
]