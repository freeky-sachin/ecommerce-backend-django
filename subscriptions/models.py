from django.db import models
from django.conf import settings

class Subscription(models.Model):
    BOX_CHOICES = [
        ('Tech', 'Tech Box'),
        ('Fashion', 'Fashion Box'),
        ('Lifestyle', 'Lifestyle Box'),
    ]
    
    FREQUENCY_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    box_type = models.CharField(max_length=50, choices=BOX_CHOICES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    next_delivery = models.DateField()
    active = models.BooleanField(default=True)
    invoice_generated = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.box_type} ({self.frequency})"
