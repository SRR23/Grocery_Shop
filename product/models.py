from django.db import models
from account.models import User
from django.db.models import Avg
import math
# Create your models here.

class Banner(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='banner')
    image_title = models.CharField(max_length=20)
    featured = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, max_length=150)
    featured = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, max_length=250)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    description = models.TextField(null=True, blank=True, default='N/A')
    in_stock = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    is_bestSelling = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.title
    
    @property
    def related(self):
        return self.category.products.all().exclude(pk=self.pk)
    
    
    def get_average_rating(self):
        average = self.product_review.aggregate(Avg('rating'))['rating__avg']
        
        if average is not None:
            return round(average)  # Round to the nearest integer
        return 0




class Review(models.Model):
    user=models.ForeignKey(User,related_name='user_review',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='product_review',on_delete=models.CASCADE)
    comment=models.TextField(max_length=250)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)],null=True)
    created_date=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.comment