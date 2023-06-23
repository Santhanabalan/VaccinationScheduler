from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('vaccination_centers/add/', views.add_vaccination_center, name='add_vaccination_center'),
    path('vaccination_centers/remove/<int:center_id>/', views.remove_vaccination_center, name='remove_vaccination_center'),
    path('vaccination_centers/<int:center_id>/', views.center_details, name='center_details'),
    path('vaccination_centers/<int:center_id>/add_slot', views.add_slot, name='add_slot'),
    path('vaccination_centers/<int:slot_id>/remove_slot', views.remove_slot, name='remove_slot'),
]
