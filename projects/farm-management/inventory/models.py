from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('adjustment', 'Adjustment'),
        ('loss', 'Loss'),
        ('transfer', 'Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='stock_movements_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movement_type} - {self.product.name}'

    class Meta:
        ordering = ['-created_at']
