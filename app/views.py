from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, UserAddress, CartItem
import logging
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'app/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Валидация данных
        if not username or not password:
            messages.error(request, 'Все поля обязательны для заполнения')
        elif password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                password=password
            )
            # Автоматически входим под новым пользователем
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('base')
    
    return render(request, 'app/register.html')

def logout_view(request):
    logout(request)
    return redirect('base')

def get_categories(request):
    """Получение всех категорий для меню"""
    return {'categories': Category.objects.all()}

def base_view(request):
    # Получаем все товары и категории
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'app/index.html', context)

def category_view(request, slug):
    """Фильтрация товаров по категории с поиском"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    search_query = request.GET.get('search', '')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query))
    
    context = {
        'category': category,
        'products': products,
        'search_query': search_query,
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

@login_required
def cart_view(request):
    # Создаем корзину, если она не существует
    cart, created = Cart.objects.get_or_create(user=request.user)
    address = UserAddress.objects.filter(user=request.user).first()
    
    context = {
        'cart': cart,
        'address': address,
    }
    return render(request, 'app/cart.html', context)

@ensure_csrf_cookie
@require_POST
@login_required
def add_to_cart(request, product_id):
    # Проверяем, что это AJAX-запрос
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется AJAX-запрос'}, 
            status=400
        )

    try:
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Товар добавлен в корзину',
            'cart_items_count': cart.items.count()
        })
    
    except Product.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Товар не найден'}, 
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)}, 
            status=500
        )

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({'status': 'success'})

@login_required
def update_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        UserAddress.objects.update_or_create(
            user=request.user,
            defaults={'address': address}
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def auth_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            # Создаем нового пользователя
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return JsonResponse({'status': 'success'})
    
    return render(request, 'app/auth.html')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.save()
        return JsonResponse({
            'status': 'success',
            'new_quantity': cart_item.quantity,
            'item_total': cart_item.total_price(),
            'cart_total': cart_item.cart.total_price()
        })
    
    return JsonResponse({'status': 'error'}, status=400)