from django.urls import path
from app.views import add_to_cart
from . import views

urlpatterns = [
    # Основные пути
    path('', views.index, name='index'),
    path('address/', views.address_page, name='address'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  
    # API endpoints
    path('api/save-address/', views.save_address, name='save_address'),
]