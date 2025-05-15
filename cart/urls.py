from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register('', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from .views import create_order_from_cart

urlpatterns += [
    path('create-order/', create_order_from_cart),
]
from .views import OrderDetailView

urlpatterns += [
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]

