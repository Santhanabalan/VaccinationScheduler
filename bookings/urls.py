from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book, name='book'),
    path('book-slot/<int:center_id>/', views.book_slot, name='book_slot'),
    path('remove_booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
]
