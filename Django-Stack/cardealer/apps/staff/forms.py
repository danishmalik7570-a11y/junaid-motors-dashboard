from django import forms
from django.contrib.auth.models import User
from .models import StaffProfile

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'


class StaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': DARK_INPUT}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': DARK_INPUT}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': DARK_INPUT}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': DARK_INPUT}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': DARK_INPUT, 'placeholder': 'Leave blank to keep current'}))

    class Meta:
        model = StaffProfile
        fields = ['role', 'phone', 'is_active']
        widgets = {
            'role': forms.Select(attrs={'class': DARK_SELECT}),
            'phone': forms.TextInput(attrs={'class': DARK_INPUT}),
        }
