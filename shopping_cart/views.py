from django.shortcuts import render

# Create your views here.

def shopping_cart_view(request):
    """ A view that renders the shopping cart contents page """

    return render(request, 'shopping_cart/shopping_cart.html')