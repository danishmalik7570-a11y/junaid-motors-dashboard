from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Q

from apps.inventory.models import Car
from apps.sales.models import Sale
from apps.installments.models import Installment
from apps.leads.models import Lead
from apps.customers.models import Customer


def get_monthly_sales_data():
    data = []
    today = timezone.now().date()
    for i in range(5, -1, -1):
        month = today.replace(day=1) - timedelta(days=i * 28)
        stats = Sale.objects.filter(
            sale_date__year=month.year,
            sale_date__month=month.month
        ).aggregate(count=Count('id'), total=Sum('total_amount'))
        data.append({
            'month': month.strftime('%b %Y'),
            'count': stats['count'] or 0,
            'revenue': float(stats['total'] or 0)
        })
    return data


@login_required
def dashboard(request):
    today = timezone.now().date()
    this_month_start = today.replace(day=1)

    car_stats = Car.objects.aggregate(
        available=Count('id', filter=Q(status='available')),
        sold=Count('id', filter=Q(status='sold')),
        reserved=Count('id', filter=Q(status='reserved')),
        repair=Count('id', filter=Q(status='under_repair')),
        slow_moving=Count('id', filter=Q(status='available', entry_date__lte=today - timedelta(days=30)))
    )

    sales_stats = Sale.objects.filter(sale_date__gte=this_month_start).aggregate(
        count=Count('id'),
        revenue=Sum('total_amount'),
        profit=Sum('profit')
    )

    installment_stats = Installment.objects.aggregate(
        pending_or_overdue=Count('id', filter=Q(status__in=['pending', 'overdue']) | Q(due_date__lt=today, status='pending')),
        overdue=Count('id', filter=Q(status='overdue') | Q(due_date__lt=today, status='pending'))
    )

    context = {
        'total_cars_available': car_stats['available'] or 0,
        'sold_this_month': sales_stats['count'] or 0,
        'pending_installments': installment_stats['pending_or_overdue'] or 0,
        'overdue_installments': installment_stats['overdue'] or 0,
        'monthly_revenue': sales_stats['revenue'] or 0,
        'monthly_profit': sales_stats['profit'] or 0,
        'new_leads': Lead.objects.filter(status='new').count(),
        'total_customers': Customer.objects.count(),
        'recent_sales': Sale.objects.select_related('car', 'customer').order_by('-sale_date')[:5],
        'low_stock_warning': (car_stats['available'] or 0) < 5,
        'today_sales': Sale.objects.filter(sale_date=today).count(),
        'slow_moving_cars': car_stats['slow_moving'] or 0,
        'monthly_sales_chart': get_monthly_sales_data(),
        'cars_available': car_stats['available'] or 0,
        'cars_sold': car_stats['sold'] or 0,
        'cars_reserved': car_stats['reserved'] or 0,
        'cars_repair': car_stats['repair'] or 0,
    }
    return render(request, 'dashboard/dashboard.html', context)
