from rest_framework import viewsets, permissions
from .models import Rental
from .serializers import RentalSerializer
from products.models import Product
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import date
from .models import Rental
from rest_framework import serializers
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_rental(request, rental_id):
    try:
        rental = Rental.objects.get(id=rental_id, user=request.user)
        if rental.is_returned:
            return Response({"message": "Already returned."}, status=400)

        rental.returned_on = date.today()
        rental.late_fee = rental.calculate_late_fee()
        rental.is_returned = True
        rental.save()

        return Response({
            "message": "Rental returned successfully.",
            "returned_on": rental.returned_on,
            "late_fee": rental.late_fee
        })
    except Rental.DoesNotExist:
        return Response({"error": "Rental not found."}, status=404)


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data.get("product")

        if not product.is_rentable:
            raise serializers.ValidationError("This product is not available for rent.")

        deposit = product.price * 0.3  # Example: 30% of price as deposit

        serializer.save(user=self.request.user, deposit=deposit)
