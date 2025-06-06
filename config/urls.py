"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app.views import remove_from_cart, update_cart_item
from app.views import register_view
from app.views import (
    base_view, category_view, product_detail,
    address_page, save_address, cart_view,
    add_to_cart, update_address, auth_view,
    login_view, logout_view, register_view  # Добавляем новые view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_view, name='base'),
    path('category/<slug:slug>/', category_view, name='category'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('address/', address_page, name='address'),
    path('save-address/', save_address, name='save_address'),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-address/', update_address, name='update_address'),
    path('auth/', auth_view, name='auth'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),  # Новый URL для входа
    path('logout/', logout_view, name='logout'),  # Новый URL для выхода
    path('register/', register_view, name='register'),  # Новый URL для регистрации
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)