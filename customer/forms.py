from django import forms
from .models import UserContact

class UserContactForm(forms.ModelForm):
    class Meta:
        model = UserContact
        fields = (('name', 'phone_number', 'address',
                  'city', 'county', 'postcode',
                  'country'))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Add a name you will rememeber',
            'phone_number': 'Phone number',
            'address': 'Address',
            'city': 'City',
            'county': 'County',
            'postcode': 'Post Code',
            'country': 'Country',
        }

        labels = {
            'name': 'Add a name you will rememeber',
            'phone_number': 'Phone number',
            'address': 'Address',
            'city': 'City',
            'county': 'County',
            'postcode': 'Post Code',
            'country': 'Country',
        }

        for field in self.fields:
            # if self.fields[field].required:
            #     placeholder = f'{placeholders[field]} *'
            # else:
            #     placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = labels[field]