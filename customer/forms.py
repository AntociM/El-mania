import phonenumbers
from django import forms
from .models import UserContact
from .models import Contact

class UserContactForm(forms.ModelForm):
    class Meta:
        model = UserContact
        fields = (('name', 'email', 'user_full_name', 'phone_number', 'address',
                  'city', 'county', 'postcode',
                  'country'))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Add a name you will rememeber',
            'user_full_name': 'Contact person',
            'email': 'Email',
            'phone_number': 'Phone number',
            'address': 'Address',
            'city': 'City',
            'county': 'County',
            'postcode': 'Post Code',
            'country': 'Country',
        }

        labels = {
            'name': 'Add a name you will rememeber',
            'user_full_name': 'Contact person',
            'email': 'Email',
            'phone_number': 'Phone number',
            'address': 'Address',
            'city': 'City',
            'county': 'County',
            'postcode': 'Post Code',
            'country': 'Country',
        }
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['user_full_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True
        self.fields['postcode'].required = True
        self.fields['country'].required = True

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders[field]
            self.fields[field].label = labels[field]
            

    def clean_user_full_name(self):
        user_full_name = self.cleaned_data['user_full_name']   

        if not all(x.isalpha() or x.isspace() for x in user_full_name):
            raise forms.ValidationError("Full name should contain only alphabetical characters. E.g. 'John Doe' ")
        return user_full_name    

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

        flag_l = False
        flag_n = False
        
        for i in address:
        
            if i.isalpha():
                flag_l = True
    
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



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'telephone', 'title', 'message']