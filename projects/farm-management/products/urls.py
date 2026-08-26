from django.urls import path

from .views import product_list

app_name = 'products'

urlpatterns = [
    path('products/', product_list, name='list'),
]
