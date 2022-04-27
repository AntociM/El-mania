from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/register_address', views.register_address, name='register_address'),
]
