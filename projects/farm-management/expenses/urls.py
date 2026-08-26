from django.urls import path

from .views import expense_list

app_name = 'expenses'

urlpatterns = [
    path('expenses/', expense_list, name='list'),
]
