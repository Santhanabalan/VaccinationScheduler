from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from bookings.models import Booking
from .forms import ProfileForm

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered successfully. Now you can login with your credentials')
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
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
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

@login_required(login_url='login')
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('home')
    return render(request, 'accounts/logout.html')
    
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

