from django import forms
from .models import Lead

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'
DARK_TEXTAREA = 'form-control'


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'source', 'interested_car', 'budget',
                  'status', 'notes', 'next_followup', 'test_drive_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': DARK_INPUT}),
            'phone': forms.TextInput(attrs={'class': DARK_INPUT}),
            'source': forms.Select(attrs={'class': DARK_SELECT}),
            'interested_car': forms.TextInput(attrs={'class': DARK_INPUT}),
            'budget': forms.NumberInput(attrs={'class': DARK_INPUT}),
            'status': forms.Select(attrs={'class': DARK_SELECT}),
            'notes': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3}),
            'next_followup': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date'}),
            'test_drive_date': forms.DateTimeInput(attrs={'class': DARK_INPUT, 'type': 'datetime-local'}),
        }
