# sales/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderItemForm


@login_required
def product_list(request):
    """បង្ហាញផលិតផល active ទាំងអស់ តម្រៀប A–Z"""
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    """បង្ហាញព័ត៌មានលម្អិតសម្រាប់ផលិតផលតែមួយ។ Return 404 ប្រសិនបើរកមិនឃើញ"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'sales/product_detail.html', {'product': product})

@login_required
def order_list(request):
    """បង្ហាញការបញ្ជាទិញទាំងអស់ ថ្មីបំផុតមុន"""
    orders = Order.objects.all()
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
def my_orders(request):
    """បង្ហាញការបញ្ជាទិញរបស់ user ដែលបាន login."""
    orders = Order.objects.filter(cashier=request.user)
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
@login_required
def create_order(request):
    """Instantly create an open order and jump straight to the add-items page."""
    order = Order.objects.create(
        cashier=request.user,
        status='open',
    )
    return redirect('add_item', pk=order.pk)


@login_required
def add_item(request, pk):
    """
    Let the cashier add line items to an open order, then mark it paid.
    """
    order = get_object_or_404(Order, pk=pk)

    status_error = None

    if request.method == 'POST':
        # Mark the order as paid
        if 'mark_paid' in request.POST and order.status == 'open':
            order.status = 'paid'
            order.save()
            return redirect('order_list')

        # Cancel the order and restore stock for all existing items
        if 'cancel_order' in request.POST and order.status == 'open':
            for item in order.items.select_related('product'):
                product = item.product
                product.stock += item.quantity
                product.save()
            order.status = 'cancelled'
            order.save()
            return redirect('order_list')

        # Prevent changes if order is already closed
        if order.status != 'open':
            status_error = 'This order is not open. You cannot add items to it.'
            item_form = OrderItemForm()
        else:
            # Add a line item
            item_form = OrderItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.order      = order
                item.unit_price = item.product.price   # snapshot the current price
                item.save()

                # Deduct stock
                product = item.product
                product.stock -= item.quantity
                product.save()

                return redirect('add_item', pk=order.pk)
    else:
        item_form = OrderItemForm()

    return render(request, 'sales/add_item.html', {
        'order':       order,
        'item_form':   item_form,
        'items':       order.items.select_related('product'),
        'status_error': status_error,
        'can_modify':  order.status == 'open',
    })
