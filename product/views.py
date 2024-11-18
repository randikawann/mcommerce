from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer
from product import serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def listproducts(request):
    query = Product.objects.all()
    serializer_class = ProductSerializer(query, many=True)
    return Response(serializer_class.data)

class ListProducts(APIView):
    def get(self, request):
        query = Product.objects.all()
        serializer_class = ProductSerializer(query, many=True)
        return Response(serializer_class.data)


class ProductDetailedView(APIView):
    def get(self, request, pid):
        query = Product.objects.filter(product_id = pid)
        serializer_class = ProductSerializer(query, many=True)
        return Response(serializer_class.data)