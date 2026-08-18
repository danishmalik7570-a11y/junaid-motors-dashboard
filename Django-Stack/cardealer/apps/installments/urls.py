from django.urls import path
from . import views

urlpatterns = [
    path('', views.installment_list, name='installment_list'),
    path('<int:pk>/mark-paid/', views.mark_paid, name='mark_paid'),
    path('<int:pk>/voucher/', views.installment_voucher, name='installment_voucher'),
]
