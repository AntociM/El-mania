from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserContactForm
from .models import UserContact


# Create your views here.

@login_required
def profile(request):

    user_contact_form = UserContactForm()
    try:
        user_contact_items = UserContact.objects.filter(user=request.user)
    except UserContact.DoesNotExist:
        user_contact_items=None

    context = {
        'register_contact_form' : user_contact_form,
        'user_contact_items': user_contact_items

    }

    return render(request, "customer/profile.html", context)


@login_required
def register_address(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')

        form = UserContactForm(request.POST)

        if form.is_valid():
            user_contact = UserContact()
            user_contact.user = request.user
            user_contact.name = form.cleaned_data['name']
            user_contact.phone_number = form.cleaned_data['phone_number']
            user_contact.address = form.cleaned_data['address']
            user_contact.city = form.cleaned_data['city']
            user_contact.county = form.cleaned_data['county']
            user_contact.postcode = form.cleaned_data['postcode']
            user_contact.country = form.cleaned_data['country']

            user_contact.save()


        return redirect(redirect_url)
    
    return render(request, "customer/profile.html")
    