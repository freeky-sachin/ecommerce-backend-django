
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    code = models.CharField(max_length=100)
    percentage = models.FloatField()
    active = models.BooleanField(default=True)
    expiry = models.DateTimeField()

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
