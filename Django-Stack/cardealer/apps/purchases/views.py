from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Purchase
from .forms import PurchaseForm


@login_required
def purchase_list(request):
    purchases = Purchase.objects.select_related('car').order_by('-purchase_date')
    return render(request, 'purchases/list.html', {'purchases': purchases})


@login_required
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save()
            purchase.car.purchase_price = purchase.purchase_price
            purchase.car.save()
            messages.success(request, 'Purchase recorded successfully.')
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'purchases/form.html', {'form': form, 'title': 'Record Purchase'})


@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'purchases/detail.html', {'purchase': purchase})
