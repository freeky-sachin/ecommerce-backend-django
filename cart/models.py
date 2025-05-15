from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models import Sum

class CartItem(models.Model):
    CART_TYPE_CHOICES = [
        ('RENT', 'Rental'),
        ('BUY', 'Purchase'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart_type = models.CharField(max_length=10, choices=CART_TYPE_CHOICES)
    start_date = models.DateField(null=True, blank=True)  # For rentals
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.cart_type})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"
