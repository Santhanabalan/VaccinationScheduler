from django import forms
from bookings.models import VaccinationCenter,VaccinationSlot

class VaccinationCenterForm(forms.ModelForm):
    class Meta:
        model = VaccinationCenter
        fields = ('name', 'address', 'from_time', 'to_time')
        widgets = {
            'from_time': forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
            'to_time': forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
        }

class VaccinationSlotForm(forms.ModelForm):
    class Meta:
        model = VaccinationSlot
        fields = ['date', 'available_slots']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
