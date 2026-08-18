from django import forms
from .models import Car, CarRepair, CarRent

DARK_INPUT = 'form-control'
DARK_SELECT = 'form-select'
DARK_TEXTAREA = 'form-control'


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'model_year', 'color', 'registration_no',
                  'purchase_price', 'selling_price', 'status', 'image', 'video', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Toyota Corolla'}),
            'model_year': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': '2023'}),
            'color': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Pearl White'}),
            'registration_no': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'ABC-123'}),
            'purchase_price': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs.'}),
            'selling_price': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs.'}),
            'status': forms.Select(attrs={'class': DARK_SELECT}),
            'image': forms.FileInput(attrs={'class': DARK_INPUT}),
            'video': forms.FileInput(attrs={'class': DARK_INPUT}),
            'notes': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3}),
        }


class CarRepairForm(forms.ModelForm):
    class Meta:
        model = CarRepair
        fields = ['car', 'workshop_name', 'work_description', 'estimated_cost',
                  'start_date', 'completion_date', 'status', 'notes']
        widgets = {
            'car': forms.Select(attrs={'class': DARK_SELECT}),
            'workshop_name': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Toyota Capital Workshop / Auto Care'}),
            'work_description': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3, 'placeholder': 'Describe repair/maintenance work (e.g. Engine tuning, bumper painting, brake overhaul)...'}),
            'estimated_cost': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs. Estimated Repair Cost'}),
            'start_date': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date'}),
            'status': forms.Select(attrs={'class': DARK_SELECT}),
            'notes': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 2, 'placeholder': 'Additional repair notes...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude sold cars from repair selection
        self.fields['car'].queryset = Car.objects.exclude(status='sold').order_by('name')


class CarRentForm(forms.ModelForm):
    class Meta:
        model = CarRent
        fields = ['car', 'date', 'city', 'total_rent', 'petrol_expense', 'total_profit', 'notes']
        widgets = {
            'car': forms.Select(attrs={'class': DARK_SELECT}),
            'date': forms.DateInput(attrs={'class': DARK_INPUT, 'type': 'date', 'id': 'id_date'}),
            'city': forms.TextInput(attrs={'class': DARK_INPUT, 'placeholder': 'e.g. Islamabad, Lahore, Murree...'}),
            'total_rent': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs. Total Rent Amount', 'id': 'id_total_rent', 'step': '0.01'}),
            'petrol_expense': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs. Petrol Expense', 'id': 'id_petrol_expense', 'step': '0.01'}),
            'total_profit': forms.NumberInput(attrs={'class': DARK_INPUT, 'placeholder': 'Rs. Net Profit', 'id': 'id_total_profit', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': DARK_TEXTAREA, 'rows': 3, 'placeholder': 'Additional notes, renter details, or remarks...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.all().order_by('name')



