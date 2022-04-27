from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/register_address', views.register_address, name='register_address'),
    path('profile/update_contact/<contact_id>', views.update_contact, name='update_contact'),
    path('profile/delete_contact/<contact_id>', views.delete_contact, name='delete_contact'),
]
