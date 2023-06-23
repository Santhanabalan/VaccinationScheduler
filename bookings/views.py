from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect
from datetime import datetime
from .models import VaccinationCenter,VaccinationSlot,Booking

# Create your views here.

def home(request):
    return render(request, 'bookings/index.html')

def book(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        search_time = request.GET.get('time')        
        
        if search_time:
            search_time = datetime.strptime(search_time, "%H:%M").time()
            centers = VaccinationCenter.objects.filter(
                Q(name__icontains=query) | Q(address__icontains=query),
                (
                    Q(from_time__lte=search_time) &
                    Q(to_time__gte=search_time)
                )
            )
        else:
            centers = VaccinationCenter.objects.filter(Q(name__icontains=query) | Q(address__icontains=query))
    else:
        centers = VaccinationCenter.objects.all()[:5]

    context = {
        'centers': centers,
        'search_time':search_time,
        'query':query
    }
    return render(request, 'bookings/book.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def remove_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user or request.user.is_staff:
        previous_page = request.META.get('HTTP_REFERER')

        if request.method == 'POST':
            slot = booking.slot
            slot.available_slots += 1
            slot.save()
            booking.delete()
            user = request.user
            messages.success(request, 'Booking removed successfully.')
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('profile')

        context = {
            'booking': booking,
            'previous_page': previous_page
        }
        return render(request, 'bookings/remove_booking_confirm.html', context)
    else:
        return redirect('home')
    
def custom_page_not_found_view(request, exception):
    context = {
        'error_title':'404',
        'error_message':"It looks like you've reached a URL that doesn't exist. Please use the navigation bar above to find your way back to our website."
    }
    return render(request, "bookings/error.html",context)

def custom_error_view(request, exception=None):
    context = {
        'error_title':'500',
        'error_message':"You found a technical glitch! Please retry again..."
    }
    return render(request, "bookings/error.html",context)

def custom_permission_denied_view(request, exception=None):
    context = {
        'error_title':'403',
        'error_message':"It seems you don't have necessary permissions."
    }
    return render(request, "bookings/error.html",context)

def custom_bad_request_view(request, exception=None):
    context = {
        'error_title':'400',
        'error_message':"You've made a bad request. Please navigate to home."
    }
    return render(request, "bookings/error.html",context)