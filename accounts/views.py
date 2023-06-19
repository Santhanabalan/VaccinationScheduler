from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render, redirect
from bookings.models import VaccinationCenter,Booking,VaccinationSlot
from .forms import VaccinationCenterForm

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
         form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def admin_dashboard(request):
    vaccination_centers = VaccinationCenter.objects.all()
    context = {
        'vaccination_centers': vaccination_centers
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def add_vaccination_center(request):
    if request.method == 'POST':
        form = VaccinationCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = VaccinationCenterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/add_vaccination_center.html', context)

def remove_vaccination_center(request, center_id):
    vaccination_center = VaccinationCenter.objects.get(pk=center_id)

    if request.method == 'POST':
        vaccination_center.delete()
        return redirect('admin_dashboard')

    context = {
        'vaccination_center': vaccination_center
    }
    return render(request, 'accounts/remove_vaccination_center.html', context)

def center_details(request, center_id):
    vaccination_center = VaccinationCenter.objects.get(pk=center_id)
    slots = VaccinationSlot.objects.filter(center=vaccination_center)
    bookings = Booking.objects.filter(slot__in=slots)
    context = {
        'vaccination_center': vaccination_center,
        'bookings': bookings
    }
    return render(request, 'accounts/center_details.html', context)

