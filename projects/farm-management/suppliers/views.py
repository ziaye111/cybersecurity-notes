from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Supplier


@login_required
@role_required('admin', 'manager')
def supplier_list(request):
    suppliers = Supplier.objects.filter(created_by=request.user)
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})
