from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Lead
from .forms import LeadForm


@login_required
def lead_list(request):
    today = timezone.now().date()
    leads = Lead.objects.all().order_by('-created_at')

    kanban = {
        'new': leads.filter(status='new'),
        'followup': leads.filter(status='followup'),
        'testdrive': leads.filter(status='testdrive'),
        'negotiating': leads.filter(status='negotiating'),
        'converted': leads.filter(status='converted'),
    }

    stats = {
        'total': leads.count(),
        'new': leads.filter(status='new').count(),
        'followup_today': leads.filter(next_followup=today).count(),
        'converted': leads.filter(status='converted').count(),
        'conversion_rate': round(leads.filter(status='converted').count() / leads.count() * 100, 1) if leads.count() > 0 else 0,
    }

    form = LeadForm()
    return render(request, 'leads/list.html', {
        'kanban': kanban,
        'stats': stats,
        'form': form,
    })


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead added successfully.')
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'leads/form.html', {'form': form, 'title': 'Add Lead'})


@login_required
def update_lead_status(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            lead.status = new_status
            lead.save()
            messages.success(request, f'Lead status updated to {new_status}.')
    return redirect('lead_list')


@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadForm(instance=lead)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated.')
            return redirect('lead_list')
    return render(request, 'leads/detail.html', {'lead': lead, 'form': form})
