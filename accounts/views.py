from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render, redirect
from bookings.models import VaccinationCenter,Booking,VaccinationSlot
from .forms import VaccinationCenterForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

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

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/admin_login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@staff_member_required(login_url="admin_login")
def admin_dashboard(request):
    vaccination_centers = VaccinationCenter.objects.all()
    context = {
        'vaccination_centers': vaccination_centers
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@staff_member_required(login_url="admin_login")
def add_vaccination_center(request):
    if request.method == 'POST':
        form = VaccinationCenterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            
            if VaccinationCenter.objects.filter(name=name, address=address).exists():
                messages.error(request, 'A vaccination center with the same name and address already exists.')
            else:
                form.save()
                messages.success(request, 'Vaccination center added successfully.')
                return redirect('admin_dashboard')
    else:
        form = VaccinationCenterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/add_vaccination_center.html', context)

@staff_member_required(login_url="admin_login")
def remove_vaccination_center(request, center_id):
    vaccination_center = VaccinationCenter.objects.get(pk=center_id)

    if request.method == 'POST':
        vaccination_center.delete()
        return redirect('admin_dashboard')

    context = {
        'vaccination_center': vaccination_center
    }
    return render(request, 'accounts/remove_vaccination_center.html', context)

@staff_member_required(login_url="admin_login")
def center_details(request, center_id):
    vaccination_center = VaccinationCenter.objects.get(pk=center_id)
    slots = VaccinationSlot.objects.filter(center=vaccination_center)
    bookings = Booking.objects.filter(slot__in=slots)
    context = {
        'vaccination_center': vaccination_center,
        'bookings': bookings
    }
    return render(request, 'accounts/center_details.html', context)

