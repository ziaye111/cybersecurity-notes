from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Expense(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    expense_date = models.DateField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='expenses_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-expense_date']
