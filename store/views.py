from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

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
             "new_price": round(offer.item.price - (offer.discount_procent * offer.item.price) / 100,2),
            #  "new_price": offer.new_price,
             "item_id":  offer.item.pk
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
    sort  = 'none'
    order = ''
    min_price = ''
    max_price = ''
    categ = None
    brand = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                # messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(category__icontains=query)
            products = products.filter(queries)
        
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortkey = sort
            # Check the order
            if 'order' in request.GET:
                order = request.GET['order']
            
            if order == 'desc':
                sortkey = f'-{sort}'

            if sort != 'none':
                products = products.order_by(sortkey)

        # Price filtering
        min_price = Decimal(request.GET.get('min_price', 0)) 
        max_price = Decimal(request.GET.get('max_price', 100000))
        # Validate the price filters
        if min_price < 0:
            messages.error(request, 'Min price cannot be negative value')
        if max_price < 0:
            messages.error(request, 'Max price cannot be negative value')
        if max_price < min_price:
            messages.warning(request, 'Max price is smaller than Min price. It may not find any products.')
        if min_price >= 0 and max_price >= 0:
            products = products.filter(price__range=(min_price, max_price))

        # Category filtering
        categ = request.GET.get('categ', '__ALL__').split('@')
        if categ[0] != '__ALL__':
            products = products.filter(category__in=categ)

        # Brand filtering
        brand = request.GET.get('brand', '__ALL__').split('@')
        if brand[0] != '__ALL__':
            products = products.filter(brand__in=brand)

    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Categories
    products_categ = products.order_by('category').values('category').distinct()
    products_brands = products.order_by('brand').values('brand').distinct()

    context = {
        'page_obj': page_obj,
        'serach_term': query,
        'current_sorting': sort,
        'current_ordering': order,
        'min_price': min_price,
        'max_price': max_price,
        'categories': products_categ,
        'selected_categories': categ,
        'product_brands': products_brands,
        'selected_brands': brand,
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


def privacy_policy(request):
    """ A view to return privacy policy page """

    return render(request, 'store/privacy_policy.html')

def terms_of_sale(request):
    """ A view to return terms of sale page """

    return render(request, 'store/terms_of_sale.html')

def open_purchase(request):
    """ A view to return open purchase page """

    return render(request, 'store/open_purchase.html')




