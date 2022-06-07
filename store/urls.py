from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    path('products', views.all_products, name='products'),
    path('products/<item_id>', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<item_id>', views.edit_product_detail, name='edit_product_detail'),
    path('products/update/<item_id>', views.update_product_detail, name='update_product_detail'),
    path('products/delete/<item_id>', views.delete_product, name='delete_product'),
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),
    path('terms_of_sale', views.terms_of_sale, name='terms_of_sale'),
    path('open_purchase', views.open_purchase, name='open_purchase'),
]

