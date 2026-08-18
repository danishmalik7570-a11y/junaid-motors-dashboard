from django import forms
import django.utils.timezone
from .models import Sale
from apps.inventory.models import Car

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'


class SaleForm(forms.ModelForm):
    sale_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date', 'id': 'id_sale_date'}),
        initial=django.utils.timezone.now().date,
        label="Sale Date"
    )

    class Meta:
        model = Sale
        fields = [
            'car', 'customer', 'sale_date', 'total_amount',
            'payment_method', 'payment_type', 'payment_status', 'payment_received',
            'down_payment', 'monthly_installment', 'installment_months', 'video'
        ]
        widgets = {
            'car': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_car'}),
            'customer': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_customer'}),
            'payment_method': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_payment_method'}),
            'payment_type': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_payment_type'}),
            'payment_status': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_payment_status'}),
            'total_amount': forms.NumberInput(attrs={'class': DARK_INPUT, 'id': 'id_total_amount', 'placeholder': '0.00', 'step': '0.01'}),
            'payment_received': forms.NumberInput(attrs={'class': DARK_INPUT, 'id': 'id_payment_received', 'value': '0', 'step': '0.01'}),
            'down_payment': forms.NumberInput(attrs={'class': DARK_INPUT, 'id': 'id_down_payment', 'value': '0', 'step': '0.01'}),
            'monthly_installment': forms.NumberInput(attrs={'class': DARK_INPUT, 'id': 'id_monthly_installment', 'value': '0', 'step': '0.01'}),
            'installment_months': forms.NumberInput(attrs={'class': DARK_INPUT, 'id': 'id_installment_months', 'value': '0', 'min': '0', 'max': '120'}),
            'video': forms.FileInput(attrs={'class': DARK_INPUT}),
        }
        labels = {
            'total_amount': 'Total Sale Price (Rs.)',
            'payment_received': 'Payment Received (Rs.)',
            'down_payment': 'Down Payment (Rs.)',
            'monthly_installment': 'Installment Amount (Rs.)',
            'installment_months': 'Total Installments',
            'payment_method': 'Payment Method',
            'payment_type': 'Sale Plan',
            'payment_status': 'Payment Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(status='available')

