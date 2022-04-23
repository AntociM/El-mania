from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        message.error(request, "There's nothing in your cart")
        return redirect(reverse('products'))

        order_form = OrderForm()
        context = { 
            'order_form': order_form,
        }

        return render(request, 'checkout/checkout.html', context)
