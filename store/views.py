from django.shortcuts import render
from .models import ItemDiscount

# Create your views here.

def index(request):
    
    """" A view to retun the index page """
    offers = ItemDiscount.objects.all()
    context = {'offers': offers}
    return render(request, 'store/index.html', context)
