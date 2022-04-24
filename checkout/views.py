from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from store.models import Item
from .forms import OrderForm
from django.conf import settings
from decimal import Decimal


# Create your views here.

def checkout(request):
    bag = request.session.get('bag', {})
    bag_items = bag.get('items', {})
    items = Item.objects.filter(pk__in=bag_items.keys())
    if not items:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('products'))

    order_form = OrderForm()


    order_total = 0
    grand_total = 0
    delivery_cost = 0
    line_item_total = 0
    cart_items = []
    for item in items:

        # Calculate item's subtotal
        line_item_total = item.price * Decimal(bag_items[f'{item.pk}'])
        # Calculate cart's subtotal
        order_total += item.price * Decimal(bag_items[f'{item.pk}'])
        cart_items.append({
            'item': item,
            'quantity': bag_items[f'{item.pk}'],
            'subtotal': line_item_total
        })

    if order_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = settings.DELIVERY_COST
    
    grand_total = order_total + delivery_cost


    context = { 
        'order_form': order_form,
        'cart_items': cart_items,
        'order_total': order_total,
        'grand_total': grand_total,
        'delivery_cost': delivery_cost
    }

    return render(request, 'checkout/checkout.html', context)
