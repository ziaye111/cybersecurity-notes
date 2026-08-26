from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from farms.models import Farm, Field


class Crop(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('harvested', 'Harvested'),
        ('cancelled', 'Cancelled'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True, related_name='crops')
    name = models.CharField(max_length=200)
    variety = models.CharField(max_length=200, blank=True)
    planted_area_hectares = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    sowing_date = models.DateField()
    expected_harvest_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='crops_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.field:
            return f'{self.name} on {self.field.name}'
        return self.name

    class Meta:
        ordering = ['-sowing_date']
