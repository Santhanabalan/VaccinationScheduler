from django.shortcuts import render
from django.contrib import messages
from .models import VaccinationCenter,VaccinationSlot,Booking
# Create your views here.

def home(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        centers = VaccinationCenter.objects.filter(name__icontains=query)
    else:
        centers = VaccinationCenter.objects.all()[:5]

    context = {
        'centers': centers
    }
    return render(request, 'bookings/index.html', context)

def book_slot(request, center_id):
    center = VaccinationCenter.objects.get(pk=center_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        slot = VaccinationSlot.objects.filter(date=date, center=center).first()

        if slot is not None:
            if slot.available_slots > 0:
                user = request.user
                if Booking.objects.filter(user=user, slot=slot).exists():
                    messages.warning(request, 'You have already booked a slot for this date.')
                else:
                    Booking.objects.create(user=user, slot=slot)
                    # slot.available_slots -= 1
                    slot.save()
                    messages.success(request, 'Slot booked successfully.')
            else:
                messages.warning(request, 'The slot for the selected date is full. Please choose another date.')
        else:
            messages.error(request, 'No booking slots available for the selected date and center.')        
    context = {
        'center': center,
    }
    return render(request, 'bookings/book_slot.html', context)
