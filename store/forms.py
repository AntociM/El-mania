from django import forms
from .models import Item

class EditItemForm(forms.ModelForm):

    class Meta:
        model = Item
    
        fields = (('name', 'category', 'description',
                   'brand', 'price', 'rating',
                   'image'))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = {
            'name': 'Item Name',
            'category': 'Item Category',
            'description': 'Short Item Description',
            'brand': 'Brand',
            'price': 'Item Price',
            'rating': 'Item Rating',
            'image': 'Item Image',
        }

        for field in self.fields:
            self.fields[field].label = labels[field]

