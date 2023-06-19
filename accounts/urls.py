from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/vaccination_centers/add/', views.add_vaccination_center, name='add_vaccination_center'),
    path('admin/vaccination_centers/remove/<int:center_id>/', views.remove_vaccination_center, name='remove_vaccination_center'),
    path('admin/vaccination_centers/<int:center_id>/', views.center_details, name='center_details'),
]
