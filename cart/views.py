from rest_framework import viewsets, permissions
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Order
from rest_framework.response import Response
from decimal import Decimal
from .serializers import OrderSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
queryset = CartItem.objects.all()

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['pk'], user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_from_cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    total = Decimal(0)
    for item in cart_items:
        total += Decimal(item.product.price) * item.quantity

    order = Order.objects.create(user=user, total_amount=total)

    # Optionally link order to cart items, or move to order items table

    # Clear cart
    cart_items.delete()

    return Response({
        "message": "Order created",
        "order_id": order.id,
        "total_amount": order.total_amount
    })

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all() 
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
