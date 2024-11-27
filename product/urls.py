from django.urls import path, include
from product import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from product.views import ListProducts, ProductDetailedView, ListProductsMixins, DetialedProductMixins, ListProductsGenerics, DetialedProductGenerics, ProductViewSet
from product.views import AdminOnlyView, CommonUserView, SharedView, UserCreateView, GuestUserView

router = DefaultRouter()

router.register(
    'productviewset', ProductViewSet, basename='product'
)

urlpatterns = [

    # Admin JWT token CREATED
    path('api/register/', UserCreateView.as_view(), name='user_create'),
    # Admin JWT token endpoints
    path('api/token/admin/', TokenObtainPairView.as_view(), name='admin_token_obtain'),
    path('api/token/admin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/token/', GuestUserView.as_view(), name='guest_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_guest'),

    # Protected APIs
    path('api/admin/', AdminOnlyView.as_view(), name='admin_only'),
    path('api/common/', CommonUserView.as_view(), name='common_user'),
    path('api/shared/', SharedView.as_view(), name='shared_api'),

    # old urls
    path('productlist/', views.listproducts, name='ListProduct'),
    path('classproductlist/', ListProducts.as_view(), name='Listproduct'),
    path('classproductlist/<int:pid>', ProductDetailedView.as_view(), name='detailedProduct'),
    path('mixinspath/', ListProductsMixins.as_view(), name='mixinsPath'),
    path('productmixin/<int:pk>', DetialedProductMixins.as_view(), name='productMixinsPath'),
    path('productgenericslist/', ListProductsGenerics.as_view(), name='listProductsGenerics'),
    path('productgenericsDetail/<int:pk>', DetialedProductGenerics.as_view(), name='productDetailsGenerics'),
    path('special/<int:pk>', views.SpecialProductGenerics.as_view(), name='specialDetailsGenerics'),
] + router.urls