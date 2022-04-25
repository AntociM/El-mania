from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from store.models import Item
from .forms import OrderForm
from django.conf import settings
from decimal import Decimal
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe


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

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

        
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=settings.BASE_URL + 'checkout/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.BASE_URL + 'checkout/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                        'images': ['https://cdn-demo.algolia.com/bestbuy/9131042_rb.jpg']
                    },
                    {
                        'name': 'T-shirt2',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                        'images': ['https://cdn-demo.algolia.com/bestbuy/9131042_rb.jpg']
                    },
                    {
                        'name': 'T-shirt3',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                        'images': ['https://cdn-demo.algolia.com/bestbuy/9131042_rb.jpg']
                    }
                ]
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return str(e)

def success(request):
    # Get session_id
    # Remove products from bag
    return render(request, 'checkout/success.html', {})

def cancelled(request):
    return render(request, 'checkout/cancelled.html', {})
