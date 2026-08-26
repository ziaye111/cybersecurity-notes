from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='farms_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Field(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=200)
    area_hectares = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.farm.name} - {self.name}'

    class Meta:
        ordering = ['name']
