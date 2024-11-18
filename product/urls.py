from django.urls import path, include
from product import views
from product.views import ListProducts, ProductDetailedView, ListProductsMixins, DetialedProductMixins, ListProductsGenerics, DetialedProductGenerics

urlpatterns = [
    path('productlist/', views.listproducts, name='ListProduct'),
    path('classproductlist/', ListProducts.as_view(), name='Listproduct'),
    path('classproductlist/<int:pid>', ProductDetailedView.as_view(), name='detailedProduct'),
    path('mixinspath/', ListProductsMixins.as_view(), name='mixinsPath'),
    path('productmixin/<int:pk>', DetialedProductMixins.as_view(), name='productMixinsPath'),
    path('productgenericslist/', ListProductsGenerics.as_view(), name='listProductsGenerics'),
    path('productgenericsDetail/<int:pk>', DetialedProductGenerics.as_view(), name='productDetailsGenerics'),
    path('special/<int:pk>', views.SpecialProductGenerics.as_view(), name='specialDetailsGenerics'),
]