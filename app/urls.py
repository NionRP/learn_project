from django.urls import path
from . import views

urlpatterns = [
    # Основные пути
    path('', views.index, name='index'),
    path('address/', views.address_page, name='address'),
    
    # API endpoints
    path('api/save-address/', views.save_address, name='save_address'),
]