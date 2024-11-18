from django.urls import path, include
from product import views
from product.views import ListProducts

urlpatterns = [
    path('productlist/', views.listproducts, name='ListProduct'),
    path('classproductlist/', ListProducts.as_view(), name='Listproduct'),
]