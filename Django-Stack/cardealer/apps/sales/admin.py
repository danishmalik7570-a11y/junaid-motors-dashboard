from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_no', 'car', 'customer', 'sale_date',
        'total_amount', 'payment_received', 'remaining_balance',
        'payment_status', 'payment_method', 'payment_type'
    ]
    list_filter = ['payment_status', 'payment_method', 'payment_type', 'sale_date']
    search_fields = ['invoice_no', 'car__name', 'customer__name', 'customer__cnic']
    date_hierarchy = 'sale_date'

    fieldsets = (
        ('Sale Information', {
            'fields': ('invoice_no', 'car', 'customer', 'sale_date', 'video')
        }),
        ('Payment Overview', {
            'fields': (
                'total_amount', 'payment_received', 'remaining_balance',
                'payment_status', 'payment_method', 'payment_type'
            )
        }),
        ('Installment Configuration', {
            'fields': (
                'down_payment', 'monthly_installment', 'installment_months',
                'installments_paid', 'installments_remaining', 'next_installment_due_date'
            )
        }),
        ('Financials', {
            'fields': ('profit',)
        })
    )

    readonly_fields = [
        'invoice_no', 'remaining_balance', 'installments_paid',
        'installments_remaining', 'next_installment_due_date', 'profit'
    ]

