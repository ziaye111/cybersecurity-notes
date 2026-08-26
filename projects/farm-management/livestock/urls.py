from django.urls import path

from .views import livestock_list

app_name = 'livestock'

urlpatterns = [
    path('livestock/', livestock_list, name='list'),
]
