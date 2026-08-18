from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from django.utils import timezone
from .models import Car, CarRepair, CarRent
from .forms import CarForm, CarRepairForm, CarRentForm
from apps.purchases.models import Purchase
from apps.sales.models import Sale


@login_required
def inventory_list(request):
    cars = Car.objects.all().order_by('-entry_date')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        cars = cars.filter(status=status_filter)
    if search:
        cars = cars.filter(
            Q(name__icontains=search) |
            Q(registration_no__icontains=search) |
            Q(color__icontains=search)
        )
    counts = {
        'available': Car.objects.filter(status='available').count(),
        'reserved': Car.objects.filter(status='reserved').count(),
        'sold': Car.objects.filter(status='sold').count(),
        'under_repair': Car.objects.filter(status='under_repair').count(),
    }
    return render(request, 'inventory/list.html', {
        'cars': cars,
        'status_filter': status_filter,
        'search': search,
        'counts': counts,
    })


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car added to inventory successfully.')
            return redirect('inventory_list')
    else:
        form = CarForm()
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Add New Car'})


@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    purchase = Purchase.objects.filter(car=car).first()
    sale = Sale.objects.filter(car=car).first()
    repairs = car.repairs.all().order_by('-start_date')
    return render(request, 'inventory/detail.html', {'car': car, 'purchase': purchase, 'sale': sale, 'repairs': repairs})


@login_required
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully.')
            return redirect('car_detail', pk=pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'inventory/form.html', {'form': form, 'title': 'Edit Car', 'car': car})


@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car_name = car.name
        try:
            car.delete()
            messages.success(request, f'Car "{car_name}" deleted from inventory.')
        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{car_name}" because it is linked to active sales or purchase records.'
            )
        return redirect('inventory_list')
    return render(request, 'inventory/confirm_delete.html', {'car': car})


def car_json(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return JsonResponse({
        'id': car.id,
        'name': str(car),
        'purchase_price': float(car.purchase_price),
        'selling_price': float(car.selling_price),
        'profit_margin': float(car.profit_margin()),
    })


# ─── Under Repair Vehicle Management ───

@login_required
def repair_list(request):
    repairs = CarRepair.objects.select_related('car').order_by('-start_date')
    active_repairs = repairs.filter(status__in=['in_progress', 'pending_parts'])
    completed_repairs = repairs.filter(status='completed')
    total_cost = repairs.aggregate(Sum('estimated_cost'))['estimated_cost__sum'] or 0

    return render(request, 'inventory/repair_list.html', {
        'repairs': repairs,
        'active_repairs': active_repairs,
        'completed_repairs': completed_repairs,
        'active_count': active_repairs.count(),
        'completed_count': completed_repairs.count(),
        'total_cost': total_cost,
    })


@login_required
def add_repair(request):
    car_id = request.GET.get('car_id')
    initial_data = {}
    if car_id:
        car = get_object_or_404(Car, pk=car_id)
        initial_data['car'] = car
    initial_data['start_date'] = timezone.now().date()

    if request.method == 'POST':
        form = CarRepairForm(request.POST)
        if form.is_valid():
            repair = form.save()
            messages.success(request, f'Vehicle "{repair.car.name}" has been logged for repair at {repair.workshop_name}. Status set to Under Repair.')
            return redirect('repair_list')
    else:
        form = CarRepairForm(initial=initial_data)

    return render(request, 'inventory/repair_form.html', {
        'form': form,
        'title': 'Under Repair Vehicle Registration',
    })


@login_required
def edit_repair(request, pk):
    repair = get_object_or_404(CarRepair, pk=pk)
    if request.method == 'POST':
        form = CarRepairForm(request.POST, instance=repair)
        if form.is_valid():
            repair = form.save()
            messages.success(request, f'Repair record for "{repair.car.name}" updated.')
            return redirect('repair_list')
    else:
        form = CarRepairForm(instance=repair)

    return render(request, 'inventory/repair_form.html', {
        'form': form,
        'title': 'Edit Repair Record',
        'repair': repair,
    })


@login_required
def complete_repair(request, pk):
    repair = get_object_or_404(CarRepair, pk=pk)
    repair.status = 'completed'
    if not repair.completion_date:
        repair.completion_date = timezone.now().date()
    repair.save()
    messages.success(request, f'Repair for "{repair.car.name}" marked as Completed! Vehicle is now set to Available status.')
    return redirect('repair_list')


# ─── Streamlined Car Rentals Management ───

@login_required
def rent_list(request):
    rentals = CarRent.objects.select_related('car').order_by('-date', '-pk')
    search = request.GET.get('search', '')
    if search:
        rentals = rentals.filter(
            Q(car__name__icontains=search) |
            Q(car__registration_no__icontains=search) |
            Q(city__icontains=search) |
            Q(notes__icontains=search)
        )

    total_rent_sum = rentals.aggregate(Sum('total_rent'))['total_rent__sum'] or 0
    petrol_expense_sum = rentals.aggregate(Sum('petrol_expense'))['petrol_expense__sum'] or 0
    total_profit_sum = rentals.aggregate(Sum('total_profit'))['total_profit__sum'] or 0

    return render(request, 'inventory/rent_list.html', {
        'rentals': rentals,
        'search': search,
        'total_count': rentals.count(),
        'total_rent_sum': total_rent_sum,
        'petrol_expense_sum': petrol_expense_sum,
        'total_profit_sum': total_profit_sum,
    })


@login_required
def add_rent(request):
    car_id = request.GET.get('car_id')
    initial_data = {'date': timezone.now().date()}
    if car_id:
        car = get_object_or_404(Car, pk=car_id)
        initial_data['car'] = car

    if request.method == 'POST':
        form = CarRentForm(request.POST)
        if form.is_valid():
            rent = form.save()
            messages.success(request, f'Car rent record for "{rent.car.name}" in {rent.city} created successfully.')
            return redirect('rent_list')
    else:
        form = CarRentForm(initial=initial_data)

    return render(request, 'inventory/rent_form.html', {
        'form': form,
        'title': 'Add New Car Rent Record',
        'is_edit': False,
    })


@login_required
def edit_rent(request, pk):
    rent = get_object_or_404(CarRent, pk=pk)
    if request.method == 'POST':
        form = CarRentForm(request.POST, instance=rent)
        if form.is_valid():
            rent = form.save()
            messages.success(request, f'Car rent record #{rent.pk} updated successfully.')
            return redirect('rent_list')
    else:
        form = CarRentForm(instance=rent)

    return render(request, 'inventory/rent_form.html', {
        'form': form,
        'title': f'Edit Rent Record #{rent.pk}',
        'rent': rent,
        'is_edit': True,
    })


@login_required
def delete_rent(request, pk):
    rent = get_object_or_404(CarRent, pk=pk)
    if request.method == 'POST':
        rent.delete()
        messages.success(request, f'Rent record #{pk} deleted successfully.')
    return redirect('rent_list')


