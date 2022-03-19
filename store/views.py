from django.shortcuts import render

# Create your views here.

def index(request):
    """" A viw to retun the index page """
    
    return render(request, 'store/index.html')