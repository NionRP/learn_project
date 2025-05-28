from django.shortcuts import render

from .models import Product

def index(request):
    products = Product.object.all()
    context = {"produsts":products}
    return render(request, "app/index.html", context=context)