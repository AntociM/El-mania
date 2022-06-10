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
    """A view for the checkout page.
    The item's price, quantity and subtotal will be displayed"""

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

        discount = get_object_or_404(ItemDiscount, item=item)
        # try:
        #     discount = ItemDiscount.objects.get(item=item)
        # except:
        #     discount = None

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
        intent = stripe.PaymentIntent.create(
            amount=1400,
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return JsonResponse({"clientSecret": intent["client_secret"]})
    except Exception as e:
        return JsonResponse(error=str(e)), 403


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        redirect_url = request.GET.get("redirect_url")
        # Validate checkout forms
        form = OrderForm(request.GET)
        address_identifier = request.GET.get("address_select")

        bag = request.session.get("bag", {})
        bag_items = bag.get("items", {})
        items = Item.objects.filter(pk__in=bag_items.keys())
        stripe_cart_items = []
        cart_items = []
        order_total = 0
        grand_total = 0
        delivery_cost = 0

        for item in items:
            discount = get_object_or_404(ItemDiscount, item=item)

            real_price = item.price if discount is None else discount.new_price

            stripe_cart_items.append(
                {
                    "name": f"{item.name}",
                    "quantity": int(bag_items[f"{item.pk}"]),
                    "currency": "usd",
                    "amount": f"{int(item.price * 100)}"
                    if discount is None
                    else f"{int(discount.new_price * 100)}",
                    "images": [f"{item.image}"],
                }
            )
            cart_items.append(
                {
                    "item": item,
                    "quantity": bag_items[f"{item.pk}"],
                    "subtotal": (real_price)*Decimal(bag_items[f"{item.pk}"]),
                }
            )
            order_total += (
                item.price if discount is None else discount.new_price
            ) * Decimal(bag_items[f"{item.pk}"])
        if order_total < settings.FREE_DELIVERY_THRESHOLD:
            delivery_cost = settings.DELIVERY_COST

        grand_total = order_total + delivery_cost

        order = Order()
        if request.user.is_authenticated:
            order.user_id = request.user.pk
        order.order_total = order_total
        order.delivery_cost = delivery_cost
        order.grand_total = grand_total

        if form.is_valid():
            order.full_name = form.cleaned_data["full_name"]
            order.email = form.cleaned_data["email"]
            order.phone_number = form.cleaned_data["phone_number"]
            order.postcode = form.cleaned_data["postcode"]
            order.city = form.cleaned_data["city"]
            order.address = form.cleaned_data["address"]
            order.county = form.cleaned_data["county"]
            order.notes = form.cleaned_data["notes"]
            order.save()
        elif address_identifier != "create":
            contact_item = get_object_or_404(
                UserContact,
                pk=address_identifier
            )
            order.full_name = contact_item.user_full_name
            order.email = contact_item.email
            order.phone_number = contact_item.phone_number
            order.postcode = contact_item.postcode
            order.city = contact_item.city
            order.address = contact_item.address
            order.county = contact_item.county
            order.address = contact_item.address
            order.save()
        else:
            contact_items = []
            if request.user.is_authenticated:
                try:
                    contact_items = UserContact.objects.filter(
                        user=request.user
                    )
                except UserContact.DoesNotExist:
                    contact_items = []
            context = {
                "contact_items": contact_items,
                "order_form": form,  # Done
                "cart_items": cart_items,
                "order_total": order_total,
                "grand_total": grand_total,
                "delivery_cost": delivery_cost,
            }
            return render(request, "checkout/checkout.html", context)

        # Save the order ID to bag
        bag["order_id"] = order.order_number
        request.session["bag"] = bag

        # Process Stripe payment
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=settings.BASE_URL
                + "/checkout/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.BASE_URL + "/checkout/cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=stripe_cart_items,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return render(request, "error.html")

        return redirect(redirect_url)


def success(request):
    """Handle successful checkouts"""

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})
    items = Item.objects.filter(pk__in=bag_items.keys())

    order_id = bag.get("order_id", None)

    if order_id:
        order = get_object_or_404(Order, pk=order_id)

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
            f"Order #{order_id} confirmation",
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
        messages.error(
            request,
            'Order could not be submitted.'
            'If you made the payment, please contact us.',
        )

    # If the order succeded, take the items from the request.session bag
    # and add them into the OrderItem table
    return render(request, "checkout/success.html", {"order_id": order_id})


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
