from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer
from product import serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets
from rest_framework.authentication import TokenAuthentication

# Create your views here.

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listproducts(request):
    query = Product.objects.all()
    serializer_class = ProductSerializer(query, many=True)
    return Response(serializer_class.data)

class ListProducts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Product.objects.all()
        serializer_class = ProductSerializer(query, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        serializer_obj = ProductSerializer(data = request.data)
        if serializer_obj.is_valid(raise_exception = True):
            product_saved = serializer_obj.save()
            return Response({"success": "Product {} created successfully".format(product_saved.name)}, status=status.HTTP_200_OK)
        return Response(serializer_obj.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pid):
        query = Product.objects.filter(product_id = pid)
        serializer_class = ProductSerializer(query, many=True)
        return Response(serializer_class.data)

    def put(self, request, pid):
        product_obj = Product.objects.get(product_id = pid)
        serializer_obj = ProductSerializer(product_obj, data = request.data)
        if serializer_obj.is_valid(raise_exception = True):
            product_saved = serializer_obj.save()
            return Response({"success": "Product {} updated successfully".format(product_saved.name)}, status=status.HTTP_200_OK)
        return Response(serializer_obj.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pid):
        product_obj = Product.objects.filter(product_id = pid).delete()
        return Response({"success": "Product deleted successfully"}, status=status.HTTP_200_OK)


class ListProductsMixins(mixins.ListModelMixin, generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetialedProductMixins(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView,
                            ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def post(self, request, *args,  **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ListProductsGenerics(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DetialedProductGenerics(generics.RetrieveAPIView,
                            generics.UpdateAPIView,
                            generics.DestroyAPIView,
                            ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SpecialProductGenerics(generics.ListAPIView,
                            generics.RetrieveUpdateDestroyAPIView
                            ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer