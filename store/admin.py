from django.contrib import admin
from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'brand',
        'category',
        'price',
        'rating',
        'image'
    )

    ordering = ('name',)

admin.site.register(Item, ItemAdmin)
