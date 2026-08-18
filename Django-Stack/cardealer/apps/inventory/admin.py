from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_year', 'registration_no', 'status', 'purchase_price', 'selling_price', 'video', 'entry_date']
    list_filter = ['status', 'model_year']
    search_fields = ['name', 'registration_no', 'color']
