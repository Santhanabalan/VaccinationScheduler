from django import forms
from bookings.models import VaccinationCenter,VaccinationSlot
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class ProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

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
