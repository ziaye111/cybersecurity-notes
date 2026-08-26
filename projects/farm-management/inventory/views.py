from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import StockMovement


@login_required
@role_required('admin', 'manager')
def stock_movement_list(request):
    movements = StockMovement.objects.filter(created_by=request.user)
    return render(request, 'inventory/stock_movement_list.html', {'movements': movements})
