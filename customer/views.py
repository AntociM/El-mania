from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserContactForm, ContactForm
from .models import UserContact
from checkout.models import Order, OrderItem


# Create your views here.

@login_required
def profile(request):
    """"A view to render user's profile"""

    new_user_contact_form = UserContactForm()
    orders = Order.objects.filter(user_id=request.user.pk)
    registered_contact_forms = []
    user_orders = []

    orders = Order.objects.filter(user_id=request.user.pk)
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        user_orders.append({
            'order': order,
            'order_items': order_items
        })

    try:
        user_contact_items = UserContact.objects.filter(user=request.user)
    except UserContact.DoesNotExist:
        user_contact_items = None

    for user_contact_item in user_contact_items:
        registered_form = UserContactForm()
        registered_form.initial = {
            'name': user_contact_item.name,
            'user_full_name': user_contact_item.user_full_name,
            'email': user_contact_item.email,
            'phone_number': user_contact_item.phone_number,
            'address': user_contact_item.address,
            'city': user_contact_item.city,
            'county': user_contact_item.county,
            'postcode': user_contact_item.postcode,
            'country': user_contact_item.country,
        }

        registered_contact_forms.append(
            {
                'item': user_contact_item,
                'form': registered_form
            }
        )

    context = {
        'register_contact_form': new_user_contact_form,
        'registered_contacts': registered_contact_forms,
        'user_orders': user_orders
    }

    return render(request, "customer/profile.html", context)


@login_required
def register_address(request):
    """Save user's contact info"""

    if request.method == 'POST':
        registered_contact_forms = []
        user_orders = []

        redirect_url = request.POST.get('redirect_url')

        form = UserContactForm(request.POST)

        if form.is_valid():
            user_contact = UserContact()
            user_contact.user = request.user
            user_contact.name = form.cleaned_data['name']
            user_contact.user_full_name = form.cleaned_data['user_full_name']
            user_contact.email = form.cleaned_data['email']
            user_contact.phone_number = form.cleaned_data['phone_number']
            user_contact.address = form.cleaned_data['address']
            user_contact.city = form.cleaned_data['city']
            user_contact.county = form.cleaned_data['county']
            user_contact.postcode = form.cleaned_data['postcode']
            user_contact.country = form.cleaned_data['country']
            messages.success(request, "Address reigstered successfully.")
            user_contact.save()
            return redirect(redirect_url)

        else:
            messages.error(
                request,
                "Address could not be registered. Please check the form")
            orders = Order.objects.filter(user_id=request.user.pk)
            for order in orders:
                order_items = Order.objects.filter(order_number=order.pk)
                user_orders.append({
                    'order': order,
                    'order_items': order_items
                })

            user_contacts = []
            if request.user.is_authenticated:
                try:
                    user_contacts = UserContact.objects.filter(user=request.user)
                except UserContact.DoesNotExist:
                    user_contacts = []

            for user_contact_item in user_contacts:
                registered_form = UserContactForm()
                registered_form.initial = {
                    'name': user_contact_item.name,
                    'user_full_name': user_contact_item.user_full_name,
                    'email': user_contact_item.email,
                    'phone_number': user_contact_item.phone_number,
                    'address': user_contact_item.address,
                    'city': user_contact_item.city,
                    'county': user_contact_item.county,
                    'postcode': user_contact_item.postcode,
                    'country': user_contact_item.country,
                }

                registered_contact_forms.append(
                    {
                        'item': user_contact_item,
                        'form': registered_form
                    }
                )

            context = {
                        'register_contact_form': form,
                        'registered_contacts': registered_contact_forms,
                        'user_orders': user_orders
                     }
            return render(request, "customer/profile.html", context)

    return render(request, "customer/profile.html")


@login_required
def update_contact(request, contact_id):
    """Update user's contact information"""

    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = UserContactForm(request.POST)
        form.fields['name'].required = False

        if form.is_valid():
            contact = get_object_or_404(UserContact, pk=contact_id)
            contact.user_full_name = form.cleaned_data['user_full_name']
            contact.email = form.cleaned_data['email']
            contact.phone_number = form.cleaned_data['phone_number']
            contact.address = form.cleaned_data['address']
            contact.city = form.cleaned_data['city']
            contact.county = form.cleaned_data['county']
            contact.postcode = form.cleaned_data['postcode']
            contact.country = form.cleaned_data['country']
            messages.success(request, "Address updated successfully.")
            contact.save()
        else:
            messages.error(request, "Could not update the address.")
        return redirect(redirect_url)

    return render(request, "customer/profile.html")


def delete_contact(request, contact_id):
    """Delete contact information"""

    if request.method == "POST":
        redirect_url = request.POST.get('redirect_url')
        contact = get_object_or_404(UserContact, pk=contact_id)
        messages.success(request, f'Address "{contact.name}" has been succesfully removed.')
        contact.delete()
        return redirect(redirect_url)

    return render(request, "customer/profile.html")


def contact_view(request):
    """"Handle contact form"""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Message submitted.')
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'customer/contact.html', {'form': form})
