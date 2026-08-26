from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from expenses.models import Expense
from inventory.models import StockMovement
from sales.models import Sale


@login_required
def dashboard(request):
    profile = request.user.profile

    total_sales = Sale.objects.filter(created_by=request.user).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_expenses = Expense.objects.filter(created_by=request.user).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_stock_movements = StockMovement.objects.filter(created_by=request.user).count()
    profit = total_sales - total_expenses

    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'profile': profile,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_stock_movements': total_stock_movements,
        'profit': profit,
    })
