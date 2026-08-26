"""
URL configuration for farm_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('farms.urls', 'farms'), namespace='farms')),
    path('', include(('crops.urls', 'crops'), namespace='crops')),
    path('', include(('livestock.urls', 'livestock'), namespace='livestock')),
    path('', include(('customers.urls', 'customers'), namespace='customers')),
    path('', include(('suppliers.urls', 'suppliers'), namespace='suppliers')),
    path('', include(('products.urls', 'products'), namespace='products')),
    path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('', include(('purchases.urls', 'purchases'), namespace='purchases')),
    path('', include(('sales.urls', 'sales'), namespace='sales')),
    path('', include(('expenses.urls', 'expenses'), namespace='expenses')),
]
