from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Crop


@login_required
@role_required('admin', 'manager')
def crop_list(request):
    crops = Crop.objects.filter(created_by=request.user)
    return render(request, 'crops/crop_list.html', {'crops': crops})
