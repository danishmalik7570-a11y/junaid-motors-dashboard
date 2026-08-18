from django.contrib import admin
from .models import Installment

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'installment_no', 'due_date', 'amount', 'status', 'paid_date']
    list_filter = ['status']
