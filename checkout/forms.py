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
        # self.fields['full_name'].widget.attrs['pattern'] = [A-Za-z ]+
        self.fields['notes'].widget.attrs['hight'] = 150
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = labels[field]
    
    # def clean_full_name(self):
    #     # Nume si prenume
    #     full_name = self.cleaned_data['full_name']

    #     if not all(x.isalpha() or x.isspace() for x in full_name):
    #         raise forms.ValidationError("Full name must contain more than 6 alphabetical characters.")
    #     return full_name

    # def clean_email(self):
    #     return self.cleaned_data['email']