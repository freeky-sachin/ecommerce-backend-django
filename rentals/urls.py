from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalViewSet

router = DefaultRouter()
router.register('', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from .views import return_rental

urlpatterns += [
    path('return/<int:rental_id>/', return_rental),
]
