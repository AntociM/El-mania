from django.shortcuts import render
from .models import ItemDiscount, Item

# Create your views here.

def index(request):
    
    """" A view to retun the index page """
    offers = ItemDiscount.objects.all()
    discounted_items = []
    for offer in offers:
        offer_dict = {
             "image": offer.item.image,
             "name": offer.item.name,
             "price": offer.item.price,
             "discount": offer.discount_procent,
            #  "new_price": round(offer.item.price - (offer.discount_procent * offer.item.price) / 100,2),
             "new_price": offer.new_price,
        }
        discounted_items.append(offer_dict)
    
    context = {
        # 'offers': offers,
        'discounted_items': discounted_items,
    }
 
    return render(request, 'store/index.html', context)

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Item.objects.all()

    context = {
        'products': products[30:60],
    }

    return render(request, 'store/products.html', context)

