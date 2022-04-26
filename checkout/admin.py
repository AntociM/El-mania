from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('order_item_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin,)

    readonly_fields = ('order_number', 'created_at',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'created_at', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'city', 'address',
                'county', 'notes', 'delivery_cost',
              'order_total', 'grand_total',)

    list_display = ('order_number', 'created_at', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)