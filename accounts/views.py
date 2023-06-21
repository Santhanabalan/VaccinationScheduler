from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render, redirect
from bookings.models import VaccinationCenter,Booking,VaccinationSlot
from .forms import VaccinationCenterForm,VaccinationSlotForm,ProfileForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date

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
            messages.error(request, 'Invalid username or password')
            form = AuthenticationForm()
    else:
         form = AuthenticationForm()
    return render(request, 'accounts/login.html')

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
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'accounts/logout.html')

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
                vaccination_center=form.save()
                messages.success(request, 'Vaccination center added successfully. Slots are opened for 14 days starting today.')

                start_date = date.today()
                end_date = start_date + timedelta(days=13)
                current_date = start_date

                while current_date <= end_date:
                    if current_date.weekday() != 6: 
                        VaccinationSlot.objects.create(center=vaccination_center, date=current_date, available_slots=10)
                    else:
                        end_date += timedelta(days=1)
                    current_date += timedelta(days=1)

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
        'bookings': bookings,
        'slots':slots
    }
    return render(request, 'accounts/center_details.html', context)

@staff_member_required(login_url="admin_login")
def add_slot(request, center_id):
    center = VaccinationCenter.objects.get(pk=center_id)

    if request.method == 'POST':
        slot_form = VaccinationSlotForm(request.POST)
        if slot_form.is_valid():
            slot = slot_form.save(commit=False)
            slot.center = center
            slot.save()
            return redirect('center_details', center_id=center.id)
    else:
        slot_form = VaccinationSlotForm()

    context = {
        'center': center,
        'slot_form': slot_form
    }

    return render(request, 'accounts/add_slot.html', context)

@staff_member_required(login_url="admin_login")
def remove_slot(request, slot_id):
    slot = VaccinationSlot.objects.get(id=slot_id)
    previous_page = request.META.get('HTTP_REFERER')

    if slot is not None:
        if request.method == 'POST':
            slot.delete()
            return redirect('admin_dashboard')

        context = {
            'slot': slot,
            'previous_page': previous_page
        }
        return render(request, 'accounts/remove_slot_confirm.html', context)
    else:
        return redirect('admin_dashboard')
    
@login_required(login_url='login')
def profile(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)

    context = {
        'user': user,
        'bookings': bookings,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/edit_profile.html', context)

