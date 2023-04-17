from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from store.models import Product

def home_page(request):
    
    products = Product.objects.all().filter(is_available = True)
    context = {
        'products' : products
    }
    return render(request,'home.html',context)