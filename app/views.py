from django.shortcuts import render
from django.http import JsonResponse
from .models import UserAddress  # Модель для сохранения адресов (нужно создать)
import json

def index(request):
    products = [
    ]
    return render(request, 'app/index.html', {'products': products})

def address_page(request):
    """Страница выбора адреса"""
    return render(request, 'app/address.html')

def save_address(request):
    """API endpoint для сохранения адреса (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = data.get('address')
            
            # В реальном проекте: сохраняем адрес для текущего пользователя
            if request.user.is_authenticated:
                UserAddress.objects.update_or_create(
                    user=request.user,
                    defaults={'address': address}
                )
                return JsonResponse({'status': 'success'})
            else:
                # Для анонимных пользователей можно сохранить в сессии
                request.session['delivery_address'] = address
                return JsonResponse({'status': 'success'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error'}, status=405)