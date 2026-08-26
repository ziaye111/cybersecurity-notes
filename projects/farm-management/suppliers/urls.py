from django.urls import path

from .views import supplier_list

app_name = 'suppliers'

urlpatterns = [
    path('suppliers/', supplier_list, name='list'),
]
