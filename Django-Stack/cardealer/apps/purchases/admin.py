from django.contrib import admin
from .models import Purchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['car', 'seller_name', 'purchase_price', 'dealer_commission', 'purchase_date']
