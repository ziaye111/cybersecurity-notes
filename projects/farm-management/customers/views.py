from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Customer


@login_required
@role_required('admin', 'manager')
def customer_list(request):
    customers = Customer.objects.filter(created_by=request.user)
    return render(request, 'customers/customer_list.html', {'customers': customers})
