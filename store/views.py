from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

from .models import ItemDiscount, Item
from .forms import ItemForm

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
             "item_id":  offer.item.pk
        }
        discounted_items.append(offer_dict)

    context = {
        'discounted_items': discounted_items,
    }

    return render(request, 'store/index.html', context)


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Item.objects.all()

    # Search functionality code from Boutique Ado project - Code Institute
    query = None
    sort = 'none'
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


def add_product(request):
    """ Add products to the store """
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = Item()
            new_item.name = form.cleaned_data['name']
            new_item.category = form.cleaned_data['category']
            new_item.description = form.cleaned_data['description']
            new_item.brand = form.cleaned_data['brand']
            new_item.price = form.cleaned_data['price']
            new_item.rating = form.cleaned_data['rating']
            new_item.image = form.cleaned_data['image']
            new_item.save()

            return redirect(f'/products/{new_item.pk}')
        else:
            context = {
                'form': form,
            }

            return render(request, 'store/add_product.html', context)

    else:

        form = ItemForm()

        context = {
         'form': form,
        }

        return render(request, 'store/add_product.html', context)


def edit_product_detail(request, item_id):
    """ A view to allow superuser to edit product details """

    product = get_object_or_404(Item, pk=item_id)

    form = ItemForm()
    form.initial = {
        'name': product.name,
        'category': product.category,
        'description': product.description,
        'brand': product.brand,
        'price': product.price,
        'rating': product.rating,
        'image': product.image
    }

    context = {
        'item': product,
        'form': form,
    }

    return render(request, 'store/edit_product_detail.html', context)


def update_product_detail(request, item_id):
    """ Update product detail in the database """
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Item, pk=item_id)
            product.name = form.cleaned_data['name']
            product.category = form.cleaned_data['category']
            product.description = form.cleaned_data['description']
            product.brand = form.cleaned_data['brand']
            product.price = form.cleaned_data['price']
            product.rating = form.cleaned_data['rating']
            product.image = form.cleaned_data['image']

            product.save()

            messages.success(request, f'{product.name}" successfully updated.')
            return redirect(f'/products/{item_id}')
        else:
            messages.error(request, 'Your product was not updated.')


def delete_product(request,item_id):
    product = get_object_or_404(Item, pk=item_id)
    product.delete()

    messages.success(request, f'{product.name}" deleted.')

    return redirect((f'/products'))


def privacy_policy(request):
    """ A view to return privacy policy page """

    return render(request, 'store/privacy_policy.html')


def terms_of_sale(request):
    """ A view to return terms of sale page """

    return render(request, 'store/terms_of_sale.html')


def open_purchase(request):
    """ A view to return open purchase page """

    return render(request, 'store/open_purchase.html')


def handle_404(request, exception):
    return render(request, '404.html')
