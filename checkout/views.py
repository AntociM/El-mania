from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from cart.models import CartItem
from .forms import OrderForm

# Create your views here.

def checkout(request):
    cart_items = CartItem.objects.filter(user_id=request.user.pk)
    if not cart_items:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('products'))

    order_form = OrderForm()
    context = { 
        'order_form': order_form,
        'cart_items': cart_items,
    }

    return render(request, 'checkout/checkout.html', context)
