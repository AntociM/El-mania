from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart_view, name='shopping_cart_view')
]