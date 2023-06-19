from django.shortcuts import render

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