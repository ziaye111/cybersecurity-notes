from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales')
    invoice_number = models.CharField(max_length=100, unique=True)
    sale_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sales_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-sale_date']


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    class Meta:
        ordering = ['product__name']
