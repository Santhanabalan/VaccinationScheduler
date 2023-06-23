from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from datetime import timedelta, date
from bookings.models import VaccinationCenter,VaccinationSlot,Booking
from .forms import VaccinationCenterForm,VaccinationSlotForm

# Create your views here.

@staff_member_required(login_url="admin_login")
def admin_dashboard(request):
    vaccination_centers = VaccinationCenter.objects.all()
    context = {
        'vaccination_centers': vaccination_centers
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

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
    return render(request, 'dashboard/center_details.html', context)

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
                messages.success(request, 'Vaccination center added successfully. Slots are opened for 14 days starting today(excluding Sundays).')

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
    return render(request, 'dashboard/add_vaccination_center.html', context)

@staff_member_required(login_url="admin_login")
def remove_vaccination_center(request, center_id):
    vaccination_center = VaccinationCenter.objects.get(pk=center_id)

    if request.method == 'POST':
        vaccination_center.delete()
        messages.success(request, 'Center removed successfully')
        return redirect('admin_dashboard')

    context = {
        'vaccination_center': vaccination_center
    }
    return render(request, 'dashboard/remove_vaccination_center.html', context)

@staff_member_required(login_url="admin_login")
def add_slot(request, center_id):
    center = VaccinationCenter.objects.get(pk=center_id)

    if request.method == 'POST':
        slot_form = VaccinationSlotForm(request.POST)
        if slot_form.is_valid():
            slot = slot_form.save(commit=False)
            slot.center = center
            slot.save()
            messages.success(request, 'New slot added successfully')
            return redirect('center_details', center_id=center.id)
    else:
        slot_form = VaccinationSlotForm()

    context = {
        'center': center,
        'slot_form': slot_form
    }

    return render(request, 'dashboard/add_slot.html', context)

@staff_member_required(login_url="admin_login")
def remove_slot(request, slot_id):
    slot = VaccinationSlot.objects.get(id=slot_id)
    previous_page = request.META.get('HTTP_REFERER')

    if slot is not None:
        if request.method == 'POST':
            slot.delete()
            messages.success(request, 'Slot removed successfully')
            return redirect('admin_dashboard')

        context = {
            'slot': slot,
            'previous_page': previous_page
        }
        return render(request, 'dashboard/remove_slot_confirm.html', context)
    else:
        return redirect('admin_dashboard')

