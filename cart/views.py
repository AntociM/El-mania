from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.models import Item, ItemDiscount

# Create your views here.


def cart_view(request):
    """A view that renders the shopping cart contents page"""

    if not request.session.session_key:
        request.session.create()

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})
    items = Item.objects.filter(pk__in=bag_items.keys())
    cart_items = []

    # Parse items
    total = 0
    for item in items:
        try:
            discount = ItemDiscount.objects.get(item=item)
        except ItemDiscount.DoesNotExist:
            discount = None

        # Calculate cart's subtotal
        total += (
            item.price * Decimal(bag_items[f"{item.pk}"])
            if discount is None
            else discount.new_price * Decimal(bag_items[f"{item.pk}"])
        )
        cart_items.append(
            {
                "item": item,
                "discount": discount,
                "quantity": bag_items[f"{item.pk}"]
            }
        )

    context = {
        "cart_items": cart_items,
        "subtotal": total,
    }

    return render(request, "cart/cart.html", context)


def add_to_cart(request, item_id):
    """Add a quantity of the specified product to the shopping cart"""

    if not request.session.session_key:
        request.session.create()

    # Retrive product
    product = get_object_or_404(Item, pk=item_id)
    redirect_url = request.POST.get("redirect_url")

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})

    if item_id in list(bag_items.keys()):
        # If the user has the product in the bag, increase the quantity
        bag_items[item_id] += 1
        messages.success(
            request,
            f'Added another "{product.name}" to your bag'
        )
    else:
        # Create cart item
        bag_items[item_id] = 1
        messages.success(request, f'Added "{product.name}" to your bag')

    bag["items"] = bag_items
    request.session["bag"] = update_bag(bag)
    return redirect(redirect_url)


def adjust_quantity(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    if not request.session.session_key:
        request.session.create()

    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})
    product = get_object_or_404(Item, pk=item_id)
    redirect_url = request.POST.get("redirect_url")

    quantity = request.POST.get(f"quantity_{item_id}")

    if item_id in list(bag_items.keys()):
        if Decimal(quantity) > 0:
            bag_items[item_id] = quantity
        else:
            messages.error(
                request,
                "Quantity could not be 0. "
                "To remove the product from cart press delete.",
            )
    else:
        messages.error(
            request,
            f'Quantity for product "{product.name}" could not be'
            ' updated and it cannot be found in the shopping bag.',
        )

    bag["items"] = bag_items
    request.session["bag"] = update_bag(bag)
    return redirect(redirect_url)


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})
    bag_items = bag.get("items", {})

    try:
        del bag_items[item_id]
    except KeyError:
        pass

    bag["items"] = bag_items
    request.session["bag"] = update_bag(bag)
    return redirect(redirect_url)


def update_bag(current_bag):
    """Returns an updated cart"""

    bag_items = current_bag.get("items", {})
    items = Item.objects.filter(pk__in=bag_items.keys())

    product_count = 0

    for item in items:
        product_count += int(bag_items[f"{item.pk}"])
    current_bag["product_count"] = product_count

    return current_bag
