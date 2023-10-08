from .decorators import custom_login_required
from .forms import PatientForm
from .models import Employee, Visit, Patient
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect

def login_view(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(Q(employee_email=email) & Q(employee_password=password))
        except Employee.DoesNotExist:
            employee = None

        if employee is not None:
            print("Pracownik istnieje")
            request.session["employee_id"] = employee.id
            return redirect("index")
        else:
            print("Pracownik nie istnieje")
            messages.error(request, "Invalid email or password.")
    print("nie weszlo w zadnego ifa")
    return render(request, 'purrfectcareview/login.html')


@custom_login_required
def index(request: HttpRequest):

    employee_id = request.session.get("employee_id")
    employee = Employee.objects.get(id=employee_id)

    visits = Visit.objects.filter(visits_employee_id=employee)

    context = {
        'employee': employee,
        'visits': visits,
    }

    return render(request, 'purrfectcareview/index.html', context)

def logout_view(request: HttpRequest):
    request.session.flush()
    return render(request, 'purrfectcareview/login.html')

@custom_login_required
def patients_view(request: HttpRequest):
    
    patients = Patient.objects.all
    
    context = {
        'patients': patients
    }

    return render(request, 'purrfectcareview/patients.html', context)

@custom_login_required
def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {'patient': patient}
    return render(request, 'purrfectcareview/patient_details.html', context)

@custom_login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_view')
    else:
        form = PatientForm()
    
    context = {'form': form}
    return render(request, 'purrfectcareview/add_patient.html', context)