from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('add/', views.add_lead, name='add_lead'),
    path('<int:pk>/', views.lead_detail, name='lead_detail'),
    path('<int:pk>/update-status/', views.update_lead_status, name='update_lead_status'),
]
