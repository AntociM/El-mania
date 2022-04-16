from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('products', views.all_products, name='products')
]

