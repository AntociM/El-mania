from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from store.models import Item, ItemDiscount
from .forms import OrderForm
from .models import Order, OrderItem
from customer.models import UserContact
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

# Create your views here.


def checkout(request):
    '''A view for the checkout page.
    The item's price, quantity and subtotal will be displayed'''

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})
    items = Item.objects.filter(pk__in=bag_items.keys())
    contact_items = []

    if not items:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse("products"))

    order_form = OrderForm()

    if request.user.is_authenticated:
        try:
            contact_items = UserContact.objects.filter(user=request.user)
        except UserContact.DoesNotExist:
            contact_items = []

    order_total = 0
    grand_total = 0
    delivery_cost = 0
    line_item_total = 0
    cart_items = []
    for item in items:

        try:
            discount = ItemDiscount.objects.get(item=item)
        except ItemDiscount.DoesNotExist:
            discount = None

        # Calculate item's subtotal
        line_item_total = (
            item.price if discount is None else discount.new_price
        ) * Decimal(bag_items[f"{item.pk}"])
        # Calculate cart's subtotal
        order_total += (
            item.price * Decimal(bag_items[f"{item.pk}"])
            if discount is None
            else discount.new_price * Decimal(bag_items[f"{item.pk}"])
        )
        cart_items.append(
            {
                "item": item,
                "quantity": bag_items[f"{item.pk}"],
                "subtotal": line_item_total,
            }
        )

    if order_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = settings.DELIVERY_COST

    grand_total = order_total + delivery_cost

    context = {
        "contact_items": contact_items,
        "order_form": order_form,
        "cart_items": cart_items,
        "order_total": order_total,
        "grand_total": grand_total,
        "delivery_cost": delivery_cost,
    }

    return render(request, "checkout/checkout.html", context)


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_payment(request):
    """Create a PaymentIntent with the order amount and currency"""

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        # Reteive the bag items
        bag = request.session.get("bag", {})
        bag_items = bag.get("items", {})
        items = Item.objects.filter(pk__in=bag_items.keys())
        order_total = 0
        grand_total = 0
        delivery_cost = 0

        for item in items:
            try:
                discount = ItemDiscount.objects.get(item=item)
            except ItemDiscount.DoesNotExist:
                discount = None

            real_price = item.price if discount is None else discount.new_price

            order_total += (
                item.price if discount is None else discount.new_price
            ) * Decimal(bag_items[f"{item.pk}"])

        if order_total < settings.FREE_DELIVERY_THRESHOLD:
            delivery_cost = settings.DELIVERY_COST

        grand_total = order_total + delivery_cost

        intent = stripe.PaymentIntent.create(
            amount=f"{int(grand_total * 100)}",
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return JsonResponse({"clientSecret": intent["client_secret"]})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


def success(request):
    """Handle successful checkouts"""

    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "GET":
        payment_intent = request.GET.get('payment_intent', '')
        redirect_status = request.GET.get('redirect_status', '')

        if redirect_status == 'succeeded':
            # process order
            bag = request.session.get("bag", {})
            bag_items = bag.get("items", {})
            items = Item.objects.filter(pk__in=bag_items.keys())

            payment = stripe.PaymentIntent.retrieve(
                payment_intent,
            )

            try:
                order = Order.objects.get(payment_id=payment_intent)
            except Order.DoesNotExist:
                order = Order()

            # Populate the order
            if request.user.is_authenticated:
                order.user_id = request.user.id
            order.payment_id = payment_intent
            order.full_name = payment['shipping']['name']
            order.email = payment['receipt_email']
            order.phone_number = payment['shipping']['phone']
            order.postcode = payment['shipping']['address']['postal_code']
            order.city = payment['shipping']['address']['city']
            order.address = payment['shipping']['address']['line1']
            order.county = payment['shipping']['address']['state']
            order.country = payment['shipping']['address']['country']
            order.order_total = payment['amount']/100

            if order.order_total < settings.FREE_DELIVERY_THRESHOLD:
                order.delivery_cost = settings.DELIVERY_COST

            order.grand_total = float(order.order_total) + float(order.delivery_cost)

            order.save()

            # Save OrderItems
            for item in items:
                order_item = OrderItem()
                order_item.order = order
                order_item.item = item
                order_item.quantity = int(bag_items[f"{item.pk}"])
                order_item.save()

            # Clear the bag
            bag = {}
            request.session["bag"] = bag

            send_mail(
                f"Order #{order.pk} confirmation",
                f"""Dear {order.full_name},

    Thank you for your order! We hope that you enjoyed shopping with us.\
    Your order is being processed and we will keep you updated.
    For additional information, contact us at orders@elmania.com.

    Best regards,
    El-mania team
    """,
                "orders@elmania.com",
                [order.email],
                fail_silently=False,
            )
        else:
            pass

    else:
        messages.error(
            request,
            'Order could not be submitted.'
            'If you made the payment, please contact us.',
        )

    return render(request, "checkout/success.html", {"order_id": order.pk})


def cancelled(request):
    """If the request failed, remove the order from database, but items in the
    bag until the session expires"""

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})

    order_id = bag.get("order_id", None)

    if order_id:
        order = get_object_or_404(Order, pk=order_id)
        order.delete()

    return render(request, "checkout/cancelled.html", {})
