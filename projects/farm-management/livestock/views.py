from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Livestock


@login_required
@role_required('admin', 'manager')
def livestock_list(request):
    records = Livestock.objects.filter(created_by=request.user)
    return render(request, 'livestock/livestock_list.html', {'records': records})
