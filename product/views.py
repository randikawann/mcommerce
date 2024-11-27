from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer, UserCreateSerializer
from product import serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdminUserJWT
from .permissions import IsCommonUserJWT
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class GuestUserView(APIView):
    def post(self, request):
        username = "guest"
        password = "guest@123" 
        
        user, created = User.objects.get_or_create(username=username, defaults={"is_staff": False})
        if created:
            user.set_password(password)
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUserJWT]

    def get(self, request):
        return Response({"message": "Welcome, Admin!"})

class CommonUserView(APIView):
    permission_classes = [IsCommonUserJWT]

    def get(self, request):
        return Response({"message": "Welcome, Common User!"})


class SharedView(APIView):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:
                return Response({"message": "Hello, Admin!"})
            else:
                return Response({"message": "Hello, Common User!"})
        return Response({"message": "Unauthorized!"}, status=403)



# OLD Code below


@api_view(['GET', 'POST'])
@permission_classes([IsCommonUserJWT])
def listproducts(request):
    query = Product.objects.all()
    serializer_class = ProductSerializer(query, many=True)
    return Response(serializer_class.data)

class ListProducts(APIView):
    permission_classes = [IsCommonUserJWT]

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
    permission_classes = [IsCommonUserJWT]

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
    permission_classes = [IsCommonUserJWT]

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
    permission_classes = [IsCommonUserJWT]

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