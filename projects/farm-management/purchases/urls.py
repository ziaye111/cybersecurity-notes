from django.urls import path

from .views import purchase_list

app_name = 'purchases'

urlpatterns = [
    path('purchases/', purchase_list, name='list'),
]
