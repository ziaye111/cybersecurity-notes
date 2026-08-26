from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product
from suppliers.models import Supplier


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchases')
    invoice_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='purchases_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-purchase_date']


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_items')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cost(self):
        return self.quantity * self.unit_cost

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    class Meta:
        ordering = ['product__name']
