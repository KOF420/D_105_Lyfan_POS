from django import forms
from .models import OrderItem


class OrderItemForm(forms.ModelForm):
    """One line item to add to an order."""
    class Meta:
        model  = OrderItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        """Validation: quantity must be at least 1."""
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return qty

    def clean_product(self):
        """Validation: product must be in stock."""
        product = self.cleaned_data.get('product')
        if product and product.stock == 0:
            raise forms.ValidationError("This product is out of stock.")
        return product