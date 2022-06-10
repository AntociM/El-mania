from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name="create-checkout-session"),
    path('success/', views.success, name="success"),
    path('cancelled/', views.cancelled, name="cancelled"),
    path('create-payment-intent/', views.create_payment, name="create-payment"),
]
