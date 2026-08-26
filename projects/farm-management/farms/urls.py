from django.urls import path

from .views import farm_list

app_name = 'farms'

urlpatterns = [
    path('farms/', farm_list, name='list'),
]
