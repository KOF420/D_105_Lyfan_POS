# sales/urls.py  (updated — replace the whole file)

from django.urls import path
from . import views

urlpatterns = [
    # ── Part 1 views ──────────────────────────────────────
    path('products/',              views.product_list,   name='product_list'),
    path('products/<int:pk>/',     views.product_detail, name='product_detail'),
    path('orders/',                views.order_list,     name='order_list'),
    path('orders/mine/',           views.my_orders,      name='my_orders'),

    # ── Part 2 views (new) ────────────────────────────────
    path('orders/new/',            views.create_order,   name='create_order'),
    path('orders/<int:pk>/items/', views.add_item,       name='add_item'),
]

# Full URL examples:
# GET  /sales/orders/new/         → blank order form
# POST /sales/orders/new/         → creates order, redirects to add-items page
# GET  /sales/orders/3/items/     → add items to order #3
# POST /sales/orders/3/items/     → save a line item OR mark order as paid
