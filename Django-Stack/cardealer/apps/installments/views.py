from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Installment
from apps.sales.models import Sale


@login_required
def installment_list(request):
    today = timezone.now().date()
    Installment.objects.filter(status='pending', due_date__lt=today).update(status='overdue')

    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '').strip()

    installments = Installment.objects.select_related(
        'sale__car', 'customer'
    ).order_by('due_date')

    if status_filter:
        installments = installments.filter(status=status_filter)

    if search_query:
        installments = installments.filter(
            Q(customer__name__icontains=search_query) |
            Q(customer__phone__icontains=search_query) |
            Q(sale__car__name__icontains=search_query) |
            Q(sale__invoice_no__icontains=search_query)
        )

    # Calculate overall remaining balance across all installment sales
    all_installment_sales = Sale.objects.filter(payment_type='installment').prefetch_related('installment_set')
    total_remaining_balance = sum(s.remaining_balance for s in all_installment_sales)

    summary = {
        'total_expected': Installment.objects.filter(
            due_date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0,
        'collected': Installment.objects.filter(
            status='paid', paid_date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0,
        'overdue_amount': Installment.objects.filter(
            status='overdue').aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_count': Installment.objects.filter(status__in=['pending', 'overdue']).count(),
        'total_remaining_balance': total_remaining_balance,
    }
    return render(request, 'installments/list.html', {
        'installments': installments,
        'summary': summary,
        'status_filter': status_filter,
        'search_query': search_query,
    })


@login_required
def mark_paid(request, pk):
    installment = get_object_or_404(Installment, pk=pk)
    installment.status = 'paid'
    installment.paid_date = timezone.now().date()
    installment.save()
    messages.success(request, f'Installment #{installment.installment_no} for {installment.customer.name} marked as paid successfully.')
    return redirect('installment_voucher', pk=installment.pk)


@login_required
def installment_voucher(request, pk):
    installment = get_object_or_404(
        Installment.objects.select_related('sale__car', 'sale__customer', 'customer'),
        pk=pk
    )
    sale = installment.sale
    all_sale_installments = Installment.objects.filter(sale=sale).order_by('installment_no')

    context = {
        'installment': installment,
        'sale': sale,
        'all_installments': all_sale_installments,
        'remaining_balance': sale.remaining_balance,
        'remaining_count': sale.remaining_installments_count,
        'paid_count': sale.paid_installments_count,
        'total_paid': sale.total_paid_amount,
        'paid_pct': sale.paid_percentage,
    }
    return render(request, 'installments/voucher.html', context)
