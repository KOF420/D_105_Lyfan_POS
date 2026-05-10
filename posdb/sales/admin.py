# sales/admin.py

from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price', 'stock', 'is_active']
    list_filter   = ['category', 'is_active']
    search_fields = ['name', 'barcode']
    ordering      = ['name']


class OrderItemInline(admin.TabularInline):
    """បង្ហាញ order items ផ្ទាល់នៅក្នុងទំព័រកែ Order"""
    model  = OrderItem
    extra  = 1    # ចំនួនជួរទទេដែលបង្ហាញសម្រាប់បន្ថែម items ថ្មី
    fields = ['product', 'quantity', 'unit_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'cashier', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['cashier', 'notes']
    ordering      = ['-created_at']
    inlines       = [OrderItemInline]    # ← បង្ហាញ items នៅក្នុងទម្រង់ order