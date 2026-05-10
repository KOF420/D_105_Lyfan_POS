# posdb/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),          # /admin/  → ផ្ទាំង Django admin
    path('sales/', include('sales.urls')),    # /sales/  → បញ្ជូនទៅ sales/urls.py
]

# ឧទាហរណ៍លំហូរ URL:
# Request: GET /sales/products/3/
# ផ្គូផ្គង: path('sales/', ...) → កាត់ 'sales/' ហើយបញ្ជូន 'products/3/' ទៅ sales/urls.py
# ផ្គូផ្គង: path('products/<int:pk>/', ...) → ហៅ product_detail(request, pk=3)