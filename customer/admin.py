from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'address']

