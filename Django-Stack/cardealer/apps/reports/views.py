import csv
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, F, Q
from django.http import HttpResponse

from apps.sales.models import Sale
from apps.purchases.models import Purchase
from apps.inventory.models import Car
from apps.installments.models import Installment
from apps.customers.models import Customer


@login_required
def reports_home(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    total_sales_count = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_profit = Sale.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    
    # Inventory Valuation
    inventory_available = Car.objects.filter(status='available')
    inventory_val_cost = inventory_available.aggregate(Sum('purchase_price'))['purchase_price__sum'] or 0
    inventory_val_sale = inventory_available.aggregate(Sum('selling_price'))['selling_price__sum'] or 0
    
    # Receivables from pending/overdue installments
    pending_installments = Installment.objects.filter(status__in=['pending', 'overdue'])
    total_receivables = pending_installments.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'inventory_val_cost': inventory_val_cost,
        'inventory_val_sale': inventory_val_sale,
        'inventory_count': inventory_available.count(),
        'total_receivables': total_receivables,
        'overdue_count': Installment.objects.filter(status='overdue').count(),
    }
    return render(request, 'reports/home.html', context)


@login_required
def daily_report(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            report_date = timezone.now().date()
    else:
        report_date = timezone.now().date()

    sales = Sale.objects.filter(sale_date=report_date).select_related('car', 'customer')
    total_revenue = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_profit = sales.aggregate(Sum('profit'))['profit__sum'] or 0
    cash_sales = sales.filter(payment_type='cash')
    installment_sales = sales.filter(payment_type='installment')

    cash_revenue = cash_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    installment_down = installment_sales.aggregate(Sum('down_payment'))['down_payment__sum'] or 0

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="daily_report_{report_date}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Invoice No', 'Customer Name', 'Car Model', 'Payment Type', 'Total Amount (PKR)', 'Profit (PKR)'])
        for sale in sales:
            writer.writerow([sale.invoice_no, sale.customer.name, sale.car.name, sale.get_payment_type_display(), sale.total_amount, sale.profit])
        writer.writerow([])
        writer.writerow(['SUMMARY', '', '', '', 'Total Revenue', total_revenue])
        writer.writerow(['SUMMARY', '', '', '', 'Total Profit', total_profit])
        return response

    context = {
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'cash_count': cash_sales.count(),
        'cash_revenue': cash_revenue,
        'installment_count': installment_sales.count(),
        'installment_down': installment_down,
        'report_date': report_date,
    }
    return render(request, 'reports/daily.html', context)


@login_required
def monthly_report(request):
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    sales = Sale.objects.filter(
        sale_date__year=year,
        sale_date__month=month
    ).select_related('car', 'customer').order_by('-sale_date')

    total_revenue = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_profit = sales.aggregate(Sum('profit'))['profit__sum'] or 0
    
    # Daily breakdown for charts & summary
    daily_breakdown = sales.values('sale_date').annotate(
        daily_revenue=Sum('total_amount'),
        daily_profit=Sum('profit'),
        count=Count('id')
    ).order_by('sale_date')

    report_title = datetime(year, month, 1).strftime('%B %Y')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="monthly_report_{year}_{month:02d}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Invoice No', 'Date', 'Customer Name', 'Car Model', 'Payment Type', 'Total Amount (PKR)', 'Profit (PKR)'])
        for sale in sales:
            writer.writerow([sale.invoice_no, sale.sale_date, sale.customer.name, sale.car.name, sale.get_payment_type_display(), sale.total_amount, sale.profit])
        writer.writerow([])
        writer.writerow(['SUMMARY', '', '', '', '', 'Total Monthly Revenue', total_revenue])
        writer.writerow(['SUMMARY', '', '', '', '', 'Total Monthly Profit', total_profit])
        return response

    context = {
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'month_name': report_title,
        'selected_year': year,
        'selected_month': month,
        'years_list': range(today.year - 3, today.year + 1),
        'months_list': [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        'daily_breakdown': daily_breakdown,
    }
    return render(request, 'reports/monthly.html', context)


@login_required
def pnl_report(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    today = timezone.now().date()
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = today - timedelta(days=180)
            end_date = today
    else:
        start_date = today - timedelta(days=180)
        end_date = today

    sales = Sale.objects.filter(sale_date__gte=start_date, sale_date__lte=end_date)
    purchases = Purchase.objects.filter(purchase_date__gte=start_date, purchase_date__lte=end_date)

    total_revenue = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_profit = sales.aggregate(Sum('profit'))['profit__sum'] or 0
    total_cost = purchases.aggregate(
        total=Sum(F('purchase_price') + F('dealer_commission'))
    )['total'] or 0
    total_commission = purchases.aggregate(Sum('dealer_commission'))['dealer_commission__sum'] or 0

    profit_margin = round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0

    # Monthly breakdown for the selected window
    monthly_pnl = []
    curr = start_date.replace(day=1)
    while curr <= end_date:
        m_sales = Sale.objects.filter(sale_date__year=curr.year, sale_date__month=curr.month)
        m_rev = m_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        m_prof = m_sales.aggregate(Sum('profit'))['profit__sum'] or 0
        monthly_pnl.append({
            'month': curr.strftime('%b %Y'),
            'cars_sold': m_sales.count(),
            'revenue': m_rev,
            'profit': m_prof,
        })
        # Advance to next month
        if curr.month == 12:
            curr = curr.replace(year=curr.year + 1, month=1)
        else:
            curr = curr.replace(month=curr.month + 1)

    best_selling = Car.objects.filter(status='sold').annotate(
        sale_count=Count('sale')
    ).order_by('-sale_count')[:5]

    slow_moving = Car.objects.filter(
        status='available',
        entry_date__lte=today - timedelta(days=30)
    ).order_by('entry_date')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="pnl_report_{start_date}_to_{end_date}.csv"'
        writer = csv.writer(response)
        writer.writerow(['FINANCIAL SUMMARY', f'{start_date} to {end_date}'])
        writer.writerow(['Total Revenue (PKR)', total_revenue])
        writer.writerow(['Total Inventory Purchase Cost (PKR)', total_cost])
        writer.writerow(['Total Dealer Commissions Paid (PKR)', total_commission])
        writer.writerow(['Gross Realized Profit (PKR)', total_profit])
        writer.writerow(['Profit Margin (%)', f'{profit_margin}%'])
        writer.writerow([])
        writer.writerow(['MONTHLY BREAKDOWN'])
        writer.writerow(['Month', 'Cars Sold', 'Revenue (PKR)', 'Profit (PKR)'])
        for r in monthly_pnl:
            writer.writerow([r['month'], r['cars_sold'], r['revenue'], r['profit']])
        return response

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'total_commission': total_commission,
        'profit_margin': profit_margin,
        'monthly_pnl': monthly_pnl,
        'best_selling': best_selling,
        'slow_moving': slow_moving,
    }
    return render(request, 'reports/pnl.html', context)


@login_required
def inventory_report(request):
    today = timezone.now().date()
    cars = Car.objects.all().order_by('-entry_date')

    available_cars = cars.filter(status='available')
    sold_cars = cars.filter(status='sold')
    reserved_cars = cars.filter(status='reserved')
    repair_cars = cars.filter(status='under_repair')

    total_purchase_val = available_cars.aggregate(Sum('purchase_price'))['purchase_price__sum'] or 0
    total_selling_val = available_cars.aggregate(Sum('selling_price'))['selling_price__sum'] or 0
    potential_profit = total_selling_val - total_purchase_val

    # Stock aging breakdown
    under_30 = 0
    days_30_60 = 0
    days_60_90 = 0
    over_90 = 0

    for car in available_cars:
        days = (today - car.entry_date).days
        if days < 30:
            under_30 += 1
        elif days <= 60:
            days_30_60 += 1
        elif days <= 90:
            days_60_90 += 1
        else:
            over_90 += 1

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="inventory_valuation_report_{today}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Reg No', 'Car Name', 'Model Year', 'Status', 'Entry Date', 'Days in Stock', 'Purchase Price (PKR)', 'Selling Price (PKR)', 'Margin (PKR)'])
        for car in cars:
            writer.writerow([
                car.registration_no, car.name, car.model_year, car.get_status_display(),
                car.entry_date, car.days_in_stock(), car.purchase_price, car.selling_price, car.profit_margin()
            ])
        writer.writerow([])
        writer.writerow(['SUMMARY', '', '', '', '', '', 'Available Stock Capital', total_purchase_val, potential_profit])
        return response

    context = {
        'cars': cars,
        'available_cars': available_cars,
        'total_count': cars.count(),
        'available_count': available_cars.count(),
        'sold_count': sold_cars.count(),
        'reserved_count': reserved_cars.count(),
        'repair_count': repair_cars.count(),
        'total_purchase_val': total_purchase_val,
        'total_selling_val': total_selling_val,
        'potential_profit': potential_profit,
        'under_30': under_30,
        'days_30_60': days_30_60,
        'days_60_90': days_60_90,
        'over_90': over_90,
        'today': today,
    }
    return render(request, 'reports/inventory_report.html', context)


@login_required
def installments_report(request):
    today = timezone.now().date()
    installments = Installment.objects.select_related('sale', 'customer').order_by('due_date')

    paid_inst = installments.filter(status='paid')
    pending_inst = installments.filter(status='pending')
    overdue_inst = installments.filter(status='overdue')

    total_collected = paid_inst.aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending = pending_inst.aggregate(Sum('amount'))['amount__sum'] or 0
    total_overdue = overdue_inst.aggregate(Sum('amount'))['amount__sum'] or 0

    total_receivables = total_pending + total_overdue
    total_all = total_collected + total_receivables
    recovery_rate = round((total_collected / total_all * 100), 1) if total_all > 0 else 100.0

    # Overdue list
    overdue_list = overdue_inst.order_by('due_date')

    # Upcoming due this month
    this_month_start = today.replace(day=1)
    if today.month == 12:
        next_month_start = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month_start = today.replace(month=today.month + 1, day=1)

    due_this_month = installments.filter(
        due_date__gte=this_month_start,
        due_date__lt=next_month_start
    )
    due_this_month_amount = due_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="installments_recovery_report_{today}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Installment #', 'Voucher No', 'Customer Name', 'Invoice No', 'Due Date', 'Amount (PKR)', 'Status'])
        for inst in installments:
            writer.writerow([inst.installment_no, inst.voucher_no, inst.customer.name, inst.sale.invoice_no, inst.due_date, inst.amount, inst.get_status_display()])
        writer.writerow([])
        writer.writerow(['SUMMARY', '', '', '', 'Total Collected', total_collected])
        writer.writerow(['SUMMARY', '', '', '', 'Total Outstanding Receivables', total_receivables])
        writer.writerow(['SUMMARY', '', '', '', 'Total Overdue', total_overdue])
        return response

    context = {
        'installments': installments,
        'total_collected': total_collected,
        'total_pending': total_pending,
        'total_overdue': total_overdue,
        'total_receivables': total_receivables,
        'recovery_rate': recovery_rate,
        'overdue_list': overdue_list,
        'due_this_month_count': due_this_month.count(),
        'due_this_month_amount': due_this_month_amount,
        'today': today,
    }
    return render(request, 'reports/installments_report.html', context)
