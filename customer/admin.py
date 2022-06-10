from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import UserProfile
from .models import UserContact
from .models import Contact


# Register your models here.
@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']


admin.site.register(UserContact)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'replied']
    search_fields = ['name', 'title', 'email', 'telephone', 'message']
