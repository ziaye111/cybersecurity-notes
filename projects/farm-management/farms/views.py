from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Farm


@login_required
@role_required('admin', 'manager')
def farm_list(request):
    farms = Farm.objects.filter(created_by=request.user)
    return render(request, 'farms/farm_list.html', {'farms': farms})
