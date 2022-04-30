from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('products', views.all_products, name='products'),
    path('products/<item_id>', views.product_detail, name='product_detail'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('terms_of_sale', views.terms_of_sale, name='terms_of_sale'),
]

