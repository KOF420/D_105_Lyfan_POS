from django.db import models
from django.contrib.auth.models import User 

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food',        'អាហារ និងភេសជ្ជៈ'),
        ('electronics', 'អេឡិចត្រូនិក'),
        ('clothing',    'សម្លៀកបំពាក់'),
        ('household',   'គ្រឿងសង្ហារឹម'),
        ('other',       'ផ្សេងៗ'),
    ]

    name       = models.CharField(max_length=200)
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price      = models.DecimalField(max_digits=8, decimal_places=2)   # ឧ. 12.99
    stock      = models.PositiveIntegerField(default=0)                # ចំនួនក្នុងស្តុក
    image_url  = models.URLField(blank=True, default='', help_text='Optional image URL for the product')
    barcode    = models.CharField(max_length=50, unique=True, blank=True)
    is_active  = models.BooleanField(default=True)                     # លាក់ទំនិញឈប់លក់

    def __str__(self):
        return f"{self.name}  —  ${self.price}  (ស្តុក: {self.stock})"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    STATUS_CHOICES = [
        ('open',       'បានបើក'),
        ('paid',       'បានបង់'),
        ('refunded',   'បានសង'),
        ('cancelled',  'បានលុបចោល'),
    ]

    cashier    = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='orders',
                 )           # ឈ្មោះ ឬ ID បុគ្គលិក
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)    # កំណត់ពេលបង្កើតការបញ្ជាទិញ
    notes      = models.TextField(blank=True)

    @property
    def total(self):
        """បូករួម subtotal នៃ line item នីមួយៗក្នុងការបញ្ជាទិញនេះ"""
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"ការបញ្ជាទិញ #{self.pk}  [{self.status.upper()}]  —  ${self.total:.2f}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)   # PROTECT ការពារការលុបផលិតផលដែលមានការលក់
    quantity   = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)    # តម្លៃនៅពេលលក់

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}  @  ${self.unit_price}"