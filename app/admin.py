from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_featured', 'is_new', 'created_at')
    list_editable = ('is_featured', 'is_new')
    list_filter = ('is_featured', 'is_new', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'