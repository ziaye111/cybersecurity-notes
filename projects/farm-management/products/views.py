from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Product


@login_required
@role_required('admin', 'manager')
def product_list(request):
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'products/product_list.html', {'products': products})
