from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
]
