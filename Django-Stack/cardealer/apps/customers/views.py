from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Customer, KhattaEntry
from .forms import CustomerForm, KhattaEntryForm
from apps.sales.models import Sale
from apps.installments.models import Installment


@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    search = request.GET.get('search', '')
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(cnic__icontains=search) |
            Q(phone__icontains=search) |
            Q(city__icontains=search)
        )
    return render(request, 'customers/list.html', {'customers': customers, 'search': search})


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/form.html', {'form': form, 'title': 'Add Customer'})


@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/form.html', {'form': form, 'title': 'Edit Customer', 'customer': customer})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    sales = Sale.objects.filter(customer=customer).order_by('-sale_date')
    installments = Installment.objects.filter(customer=customer).order_by('due_date')
    return render(request, 'customers/detail.html', {
        'customer': customer,
        'sales': sales,
        'installments': installments,
    })


# ─── Khatta (Ledger / Udhar) Management ───

@login_required
def khatta_list(request):
    entries = KhattaEntry.objects.all().order_by('-date', '-pk')
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')

    if type_filter:
        entries = entries.filter(entry_type=type_filter)
    if status_filter:
        entries = entries.filter(status=status_filter)
    if search:
        entries = entries.filter(
            Q(name__icontains=search) |
            Q(note__icontains=search)
        )

    pending_entries = KhattaEntry.objects.filter(status='pending')
    total_lene_hain = pending_entries.filter(entry_type='lene_hain').aggregate(Sum('amount'))['amount__sum'] or 0
    total_dene_hain = pending_entries.filter(entry_type='dene_hain').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_lene_hain - total_dene_hain

    return render(request, 'customers/khatta_list.html', {
        'entries': entries,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'search': search,
        'total_lene_hain': total_lene_hain,
        'total_dene_hain': total_dene_hain,
        'net_balance': net_balance,
        'total_count': KhattaEntry.objects.count(),
        'pending_count': pending_entries.count(),
        'settled_count': KhattaEntry.objects.filter(status='settled').count(),
    })


@login_required
def add_khatta(request):
    initial_data = {'date': timezone.now().date(), 'entry_type': 'lene_hain'}
    if request.method == 'POST':
        form = KhattaEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, f'Khatta entry for "{entry.name}" ({entry.get_entry_type_display()}) recorded successfully.')
            return redirect('khatta_list')
    else:
        form = KhattaEntryForm(initial=initial_data)

    return render(request, 'customers/khatta_form.html', {
        'form': form,
        'title': 'New Khatta Entry',
        'is_edit': False,
    })


@login_required
def edit_khatta(request, pk):
    entry = get_object_or_404(KhattaEntry, pk=pk)
    if request.method == 'POST':
        form = KhattaEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            messages.success(request, f'Khatta entry #{entry.pk} for "{entry.name}" updated successfully.')
            return redirect('khatta_list')
    else:
        form = KhattaEntryForm(instance=entry)

    return render(request, 'customers/khatta_form.html', {
        'form': form,
        'title': f'Edit Khatta Entry #{entry.pk}',
        'entry': entry,
        'is_edit': True,
    })


@login_required
def settle_khatta(request, pk):
    entry = get_object_or_404(KhattaEntry, pk=pk)
    if request.method == 'POST':
        if entry.status == 'pending':
            entry.status = 'settled'
            entry.settled_date = timezone.now().date()
            messages.success(request, f'Khatta entry #{entry.pk} for "{entry.name}" marked as Settled / Clear!')
        else:
            entry.status = 'pending'
            entry.settled_date = None
            messages.info(request, f'Khatta entry #{entry.pk} for "{entry.name}" reverted to Pending status.')
        entry.save()
    return redirect('khatta_list')


@login_required
def delete_khatta(request, pk):
    entry = get_object_or_404(KhattaEntry, pk=pk)
    if request.method == 'POST':
        name = entry.name
        entry.delete()
        messages.success(request, f'Khatta entry for "{name}" deleted successfully.')
    return redirect('khatta_list')

