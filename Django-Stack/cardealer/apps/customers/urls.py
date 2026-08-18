from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.add_customer, name='add_customer'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.edit_customer, name='edit_customer'),
    path('khatta/', views.khatta_list, name='khatta_list'),
    path('khatta/add/', views.add_khatta, name='add_khatta'),
    path('khatta/<int:pk>/edit/', views.edit_khatta, name='edit_khatta'),
    path('khatta/<int:pk>/settle/', views.settle_khatta, name='settle_khatta'),
    path('khatta/<int:pk>/delete/', views.delete_khatta, name='delete_khatta'),
]

