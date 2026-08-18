from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from .models import Sale
from .forms import SaleForm
from apps.inventory.models import Car
from apps.customers.models import Customer
from apps.customers.forms import CustomerForm
from apps.installments.models import Installment


@login_required
def sales_list(request):
    sales = Sale.objects.select_related('car', 'customer').order_by('-sale_date')
    return render(request, 'sales/list.html', {'sales': sales})


@login_required
def new_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.profit = sale.total_amount - sale.car.purchase_price
            sale.save()
            if sale.payment_type == 'installment' and sale.installment_months > 0:
                for i in range(1, sale.installment_months + 1):
                    due = sale.sale_date + timedelta(days=30 * i)
                    Installment.objects.create(
                        sale=sale,
                        customer=sale.customer,
                        installment_no=i,
                        due_date=due,
                        amount=sale.monthly_installment,
                        status='pending'
                    )
            messages.success(request, f'Sale recorded. Invoice: {sale.invoice_no}')
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    available_cars = Car.objects.filter(status='available')
    customers = Customer.objects.all()
    customer_form = CustomerForm()
    return render(request, 'sales/new_sale.html', {
        'form': form,
        'available_cars': available_cars,
        'customers': customers,
        'customer_form': customer_form,
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    installments = Installment.objects.filter(sale=sale).order_by('installment_no')
    return render(request, 'sales/detail.html', {'sale': sale, 'installments': installments})


@login_required
def sale_invoice(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    installments = Installment.objects.filter(sale=sale).order_by('installment_no')
    return render(request, 'sales/invoice.html', {'sale': sale, 'installments': installments})
