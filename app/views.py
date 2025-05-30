from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-created_at')  
    return render(request, 'app/index.html', {'products': products})