from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'source', 'interested_car', 'status', 'created_at']
    list_filter = ['status', 'source']
