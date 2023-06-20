from django import forms
from bookings.models import VaccinationCenter,VaccinationSlot

class VaccinationCenterForm(forms.ModelForm):
    class Meta:
        model = VaccinationCenter
        fields = ('name', 'address', 'from_time', 'to_time')

class VaccinationSlotForm(forms.ModelForm):
    class Meta:
        model = VaccinationSlot
        fields = ['date', 'available_slots']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
