from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('daily/', views.daily_report, name='daily_report'),
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('pnl/', views.pnl_report, name='pnl_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('installments/', views.installments_report, name='installments_report'),
]
