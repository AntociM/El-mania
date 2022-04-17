from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

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
    
    ### Search functionality code from Boutique Ado project - Code Institute
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(category__icontains=query)
            products = products.filter(queries)
    
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'serach_term': query,
    }

    return render(request, 'store/products.html', context)

def product_detail(request, item_id):
    """ A view to show individual product details """
    print(item_id)

    product = get_object_or_404(Item, pk=item_id)

    context = {
        'product': product,
    }

    return render(request, 'store/product_detail.html', context)




