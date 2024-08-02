from django.db import models

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Discount in Percentage")
    active = models.BooleanField(default=True)
    miniAmountToUseCoupon = models.PositiveBigIntegerField(default="100")
    active_date = models.DateField()
    expiry_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.code