from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart_view, name='shopping_cart_view'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<cart_item_id>/', views.adjust_quantity, name='adjust_quantity')
]