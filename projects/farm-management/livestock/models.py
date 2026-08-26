from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from farms.models import Farm


class Livestock(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('cow', 'Cow'),
        ('goat', 'Goat'),
        ('sheep', 'Sheep'),
        ('poultry', 'Poultry'),
        ('pig', 'Pig'),
    ]

    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('breeding', 'Breeding'),
        ('sold', 'Sold'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='livestock')
    animal_type = models.CharField(max_length=30, choices=ANIMAL_TYPE_CHOICES)
    breed = models.CharField(max_length=200)
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    age_months = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='healthy')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='livestock_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.breed} {self.animal_type}'

    class Meta:
        ordering = ['breed']
