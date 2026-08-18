from django import forms
from .models import Customer, KhattaEntry

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'
DARK_TEXTAREA = 'form-control'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'cnic', 'phone', 'address', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Ali Khan'}),
            'cnic': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': '35201-1234567-1'}),
            'phone': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': '0300-1234567'}),
            'address': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 2}),
            'city': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Lahore'}),
        }


class KhattaEntryForm(forms.ModelForm):
    class Meta:
        model = KhattaEntry
        fields = ['name', 'entry_type', 'amount', 'note', 'date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Ali Khan / Ahmed Raza'}),
            'entry_type': forms.Select(attrs={'class': DARK_SELECT, 'id': 'id_entry_type'}),
            'amount': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs. Amount in PKR', 'step': '0.01'}),
            'note': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3, 'placeholder': 'e.g. Car repair ke paisay lene hain / Car purchase remaining payment...'}),
            'date': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date', 'id': 'id_date'}),
            'status': forms.Select(attrs={'class': DARK_SELECT}),
        }
