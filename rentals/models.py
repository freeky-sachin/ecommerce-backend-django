from django.db import models
from django.conf import settings
from products.models import Product

class Rental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    is_returned = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    invoice_generated = models.BooleanField(default=False)
    returned_on = models.DateField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_late_fee(self):
        if self.end_date and self.returned_on and self.returned_on > self.end_date:
            days_late = (self.returned_on - self.end_date).days
            return days_late * 50  # ₹50 per day late fee
        return 0

    def __str__(self):
        return f"{self.user.username} rented {self.product.name}"
