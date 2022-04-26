from django.shortcuts import render

# Create your views here.

def profile(request):
    """ Display of user's profile """
    template = "customer/profile.html"
    context = {}

    return render(request, template, context)
