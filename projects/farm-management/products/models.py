from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('bag', 'Bag'),
        ('crate', 'Crate'),
        ('piece', 'Piece'),
        ('liter', 'Liter'),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
