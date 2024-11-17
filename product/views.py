from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer
from product import serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def listproducts(request):
    query = Product.objects.all()
    serializer_class = ProductSerializer(query, many=True)
    return Response(serializer_class.data)