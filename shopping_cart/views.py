from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Item
from .models import CartItem
from datetime import datetime

# Create your views here.

def shopping_cart_view(request):
    """ A view that renders the shopping cart contents page """
    cart_items = CartItem.objects.filter(user_id=request.user.pk)

    # Calculate cart's subtotal
    total = 0
    for cart_item in cart_items:
         total = (cart_item.item.price * cart_item.quantity) + total

        
    context = {
        'cart_items' : cart_items,
        'subtotal': total,
    }

    return render(request, 'shopping_cart/shopping_cart.html', context)


def add_to_cart(request, item_id):
    # Retrive product
    product = get_object_or_404(Item, pk=item_id)
    redirect_url = request.POST.get('redirect_url')

    if not request.user.is_authenticated:
        print("User is not authenticated")

    try:
        # If the user has the product in the bag, increase the quantity
        current_items = CartItem.objects.get(user_id=request.user.pk, item=product)
        current_items.quantity += 1
        current_items.save()
    except ObjectDoesNotExist:
        # Create cart item
        cart_item = CartItem()
        cart_item.item = product
        cart_item.user_id = request.user.pk
        cart_item.quantity = 1
        cart_item.total = 0
        cart_item.created_at = datetime.now()
        cart_item.modified_at = datetime.now()
        cart_item.save()

    return redirect(redirect_url)
