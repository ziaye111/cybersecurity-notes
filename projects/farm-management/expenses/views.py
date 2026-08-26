from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import role_required

from .models import Expense


@login_required
@role_required('admin', 'manager')
def expense_list(request):
    expenses = Expense.objects.filter(created_by=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})
