from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_car, name='add_car'),
    path('<int:pk>/', views.car_detail, name='car_detail'),
    path('<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('<int:pk>/delete/', views.delete_car, name='delete_car'),
    path('<int:pk>/json/', views.car_json, name='car_json'),
    path('repairs/', views.repair_list, name='repair_list'),
    path('repairs/add/', views.add_repair, name='add_repair'),
    path('repairs/<int:pk>/edit/', views.edit_repair, name='edit_repair'),
    path('repairs/<int:pk>/complete/', views.complete_repair, name='complete_repair'),
    path('rentals/', views.rent_list, name='rent_list'),
    path('rentals/add/', views.add_rent, name='add_rent'),
    path('rentals/<int:pk>/edit/', views.edit_rent, name='edit_rent'),
    path('rentals/<int:pk>/delete/', views.delete_rent, name='delete_rent'),
]



