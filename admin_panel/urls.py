from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, DiscountViewSet, TransactionViewSet, CustomerViewSet,
    UploadProductImage
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('products/<int:pk>/upload-images/', UploadProductImage.as_view(), name='upload-images'),
]
