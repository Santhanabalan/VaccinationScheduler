from django.contrib import admin
from .models import VaccinationCenter,VaccinationSlot,Booking
# Register your models here.
admin.site.register(VaccinationCenter)
admin.site.register(VaccinationSlot)
admin.site.register(Booking)