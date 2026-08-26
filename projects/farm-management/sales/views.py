from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Sale


@login_required
@role_required('admin', 'manager')
def sale_list(request):
    sales = Sale.objects.filter(created_by=request.user)
    return render(request, 'sales/sale_list.html', {'sales': sales})
