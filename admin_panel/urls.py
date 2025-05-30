# admin_panel/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, DiscountViewSet, TransactionViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('api/admin/', include(router.urls)),
]
