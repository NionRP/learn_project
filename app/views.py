from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UserAddress, Product, Category
import json

def get_categories(request):
    """Получение всех категорий для меню"""
    return {'categories': Category.objects.all()}

def base_view(request):
    """Главная страница с товарами"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    context.update(get_categories(request))
    return render(request, 'app/index.html', context)

def category_view(request, slug):
    """Фильтрация товаров по выбранной категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products,
    }
    context.update(get_categories(request))
    return render(request, 'app/index.html', context)

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