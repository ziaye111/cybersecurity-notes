from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Purchase


@login_required
@role_required('admin', 'manager')
def purchase_list(request):
    purchases = Purchase.objects.filter(created_by=request.user)
    return render(request, 'purchases/purchase_list.html', {'purchases': purchases})
