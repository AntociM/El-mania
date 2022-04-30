import phonenumbers
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
    
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']

        if not all(x.isalpha() or x.isspace() for x in full_name):
            raise forms.ValidationError("Full name should contain only alphabetical characters. E.g. 'John Doe' ")
        return full_name

    def clean_city(self):
        city = self.cleaned_data['city']

        if not all(x.isalpha() or x.isspace() for x in city):
            raise forms.ValidationError("City should contain only alphabetical characters. E.g. 'Stockholm' ")
        return city

    def clean_county(self):
        county = self.cleaned_data['county']

        if county != None and not all(x.isalpha() or x.isspace() for x in county):
            raise forms.ValidationError("County should contain only alphabetical characters. E.g. 'Stockholm Lan' ")
        return county

    def clean_address(self):
        address = self.cleaned_data['address']

        # initializing flag variable
        flag_l = False
        flag_n = False
        
        for i in address:
        
            # if string has letter
            if i.isalpha():
                flag_l = True
    
            # if string has number
            if i.isdigit():
                flag_n = True

        if not flag_l:
            raise forms.ValidationError("Address street number not detected. E.g. '1984 Motihari Blvd, Ste 101' ")
        elif not flag_n:
            raise forms.ValidationError("Address street name not detected. E.g. '1984 Motihari Blvd, Ste 101' ")

        return address


    def clean_phone_number(self):
        string_phone_number = self.cleaned_data['phone_number']
        try:
            phone_number = phonenumbers.parse(string_phone_number)
            if not phonenumbers.is_valid_number(phone_number):
                raise forms.ValidationError("Phone number is invalid.")
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Phone number is not in a valid format. E.g. +46712345678 ")
        return string_phone_number



