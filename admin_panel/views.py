# admin_panel/views.py

from rest_framework import viewsets
from .models import Product, Discount, Transaction, Customer
from .serializers import ProductSerializer, DiscountSerializer, TransactionSerializer, CustomerSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductImage
from .serializers import ProductImageSerializer

class UploadProductImage(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        product = Product.objects.get(id=pk)
        images = request.FILES.getlist('images')  # multiple images
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
