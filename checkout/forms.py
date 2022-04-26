from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (('full_name', 'email', 'phone_number',
                  'address', 'city', 'postcode',
                  'county', 'country', 'notes' ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'city': 'Town or City',
            'address': 'Street address',
            'county': 'County',
            'notes': 'Notes'
        }

        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'city': 'Town or City',
            'address': 'Street address',
            'county': 'County',
            'notes': 'Notes'
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        self.fields['notes'].widget.attrs['hight'] = 150
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = labels[field]
