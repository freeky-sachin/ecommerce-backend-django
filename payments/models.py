from django.db import models
from django.conf import settings
from rentals.models import Rental
from subscriptions.models import Subscription
from cart.models import Order

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    payment_intent = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency}"
