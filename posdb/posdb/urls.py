# posdb/urls.py  (updated)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('',          RedirectView.as_view(url='/accounts/login/'), name='home'),  # / → login page"
    path('admin/',    admin.site.urls),
    path('sales/',    include('sales.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password change
]

# URL map:
# /                  → redirect to /accounts/login/
# /accounts/login/   → login page
# /accounts/logout/  → logs the user out
# /sales/products/   → product catalogue  (requires login)
# /sales/orders/     → orders list        (requires login)
# /admin/            → Django admin panel
