from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserContactForm
from .models import UserContact


# Create your views here.

@login_required
def profile(request):

    new_user_contact_form = UserContactForm()
    registered_contact_forms = []
    try:
        user_contact_items = UserContact.objects.filter(user=request.user)
    except UserContact.DoesNotExist:
        user_contact_items=None

    for user_contact_item in user_contact_items:
        registered_form = UserContactForm()
        registered_form.initial = {
            'name' : user_contact_item.name,
            'phone_number' : user_contact_item.phone_number,
            'address' : user_contact_item.address,
            'city' : user_contact_item.city,
            'county' : user_contact_item.county,
            'postcode' : user_contact_item.postcode,
            'country' : user_contact_item.country,
        }

        registered_contact_forms.append(
            {
                'item': user_contact_item,
                'form' : registered_form
            }
        )

    context = {
        'register_contact_form' : new_user_contact_form,
        'registered_contacts': registered_contact_forms
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

@login_required
def update_contact(request, contact_id):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        form = UserContactForm(request.POST)

        if form.is_valid():
            contact = get_object_or_404(UserContact, pk=contact_id)

            contact.phone_number = form.cleaned_data['phone_number']
            contact.address = form.cleaned_data['address']
            contact.city = form.cleaned_data['city']
            contact.county = form.cleaned_data['county']
            contact.postcode = form.cleaned_data['postcode']
            contact.country = form.cleaned_data['country']
            contact.save()
        return redirect(redirect_url)
        

    return render(request, "customer/profile.html")

def delete_contact(request, contact_id): 
    if request.method == "POST":
        redirect_url = request.POST.get('redirect_url')
        contact = get_object_or_404(UserContact, pk=contact_id)
        messages.success(request, f'Address "{contact.name}" has been succesfully removed.')
        contact.delete()
        return redirect(redirect_url)

    # messages.success(request, f'Saved address "{contact.name}" has been succesfully removed.')
    return render(request, "customer/profile.html")


        
