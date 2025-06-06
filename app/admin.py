from django.contrib import admin
from .models import MainAd, ProductAd
from .models import Product, Category

admin.site.register(Product)
admin.site.register(Category)
@admin.register(MainAd)
class MainAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_editable = ('is_active',)

@admin.register(ProductAd)
class ProductAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_editable = ('is_active',)