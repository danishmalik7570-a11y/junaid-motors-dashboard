from django import forms
from .models import Purchase

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'
DARK_TEXTAREA = 'form-control'


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['car', 'seller_name', 'seller_phone', 'purchase_price',
                  'dealer_commission', 'document', 'purchase_date', 'notes']
        widgets = {
            'car': forms.Select(attrs={'class': DARK_SELECT}),
            'seller_name': forms.TextInput(attrs={'class': DARK_INPUT}),
            'seller_phone': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': '03XX-XXXXXXX'}),
            'purchase_price': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs.'}),
            'dealer_commission': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs.'}),
            'purchase_date': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3}),
        }
