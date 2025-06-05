from django.shortcuts import render
from django.http import JsonResponse
from .models import UserAddress, Product, Category
import json

def get_categories(request):
    """Вспомогательная функция для получения категорий"""
    return {'categories': Category.objects.all()}

def base_view(request):
    """Главная страница (ранее index)"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
    }
    context.update(get_categories(request))
    return render(request, 'app/index.html', context)

def category_view(request, slug):
    """Отображение товаров по категории"""
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products,
    }
    context.update(get_categories(request))
    return render(request, 'app/category.html', context)

def address_page(request):
    """Страница выбора адреса"""
    context = {}
    context.update(get_categories(request))  # Добавляем категории
    return render(request, 'app/address.html', context)

def save_address(request):
    """API endpoint для сохранения адреса (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = data.get('address')
            
            if request.user.is_authenticated:
                UserAddress.objects.update_or_create(
                    user=request.user,
                    defaults={'address': address}
                )
                return JsonResponse({'status': 'success'})
            else:
                request.session['delivery_address'] = address
                return JsonResponse({'status': 'success'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error'}, status=405)

def product_detail(request, id):
    """Страница деталей товара"""
    product = Product.objects.get(id=id)
    context = {
        'product': product,
    }
    context.update(get_categories(request))
    return render(request, 'app/product_detail.html', context)