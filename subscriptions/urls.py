from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet

router = DefaultRouter()
router.register('', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
