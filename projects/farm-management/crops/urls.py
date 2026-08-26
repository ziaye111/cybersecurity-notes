from django.urls import path

from .views import crop_list

app_name = 'crops'

urlpatterns = [
    path('crops/', crop_list, name='list'),
]
