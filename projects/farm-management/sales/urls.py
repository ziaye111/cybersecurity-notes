from django.urls import path

from .views import sale_list

app_name = 'sales'

urlpatterns = [
    path('sales/', sale_list, name='list'),
]
