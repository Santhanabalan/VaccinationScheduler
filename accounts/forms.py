from django import forms
from bookings.models import VaccinationCenter

class VaccinationCenterForm(forms.ModelForm):
    class Meta:
        model = VaccinationCenter
        fields = ('name', 'address', 'from_time', 'to_time')
