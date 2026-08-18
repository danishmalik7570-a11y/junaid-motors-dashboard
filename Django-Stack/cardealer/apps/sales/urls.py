from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('new/', views.new_sale, name='new_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/invoice/', views.sale_invoice, name='sale_invoice'),
]
