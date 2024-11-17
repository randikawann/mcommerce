from django.urls import path, include
from product import views

urlpatterns = [
    path('productlist/', views.listproducts, name='ListProduct'),
]