from django.urls import path

from .views import stock_movement_list

app_name = 'inventory'

urlpatterns = [
    path('inventory/', stock_movement_list, name='list'),
]
