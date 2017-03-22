from django.shortcuts import render, get_object_or_404
from .models import RoomInspectionForm, Student, ResidenceHall, RA
from django.utils import timezone

# Create your views here.

#return a collection
def forms_list(request):
    forms = RoomInspectionForm.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'rapp/forms_list.html', {'forms': forms})

#return ONE instance
def form_detail(request, pk):
    form = get_object_or_404(RoomInspectionForm, pk=pk)
    return render(request, 'rapp/form_detail.html', {'form': form}) 

def dashboard(request):
    return render(request, 'rapp/dashboard.html')

def halls_list(request, pk):
    students = Student.objects.filter(status__pk=pk)
    return render(request, 'rapp/residence_hall.html', {'students': students}) 

def ra_list(request):
    ras = RA.objects.all()
    return render(request, 'rapp/ra_list.html', {'ras': ras})

def logout(request):
    return render(request, 'rapp/logout.html')
