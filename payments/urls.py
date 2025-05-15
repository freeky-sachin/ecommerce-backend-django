from django.urls import path
from .views import CreateStripePaymentIntent
from .views import stripe_webhook
from .views import CreateStripePaymentIntent, stripe_webhook, download_invoice, invoice_ready

urlpatterns = [
    path('stripe/', CreateStripePaymentIntent.as_view(), name='stripe-payment'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('invoice/', download_invoice),
    path('invoice-ready/', invoice_ready),


]

from .views import download_invoice

urlpatterns += [
    path('invoice/<int:payment_id>/', download_invoice, name='download-invoice'),
]
