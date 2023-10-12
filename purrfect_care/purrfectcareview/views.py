
from .forms import PatientForm
from .models import Employee, Visit, Patient, Owner
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import OwnerSerializer, PatientSerializer, VisitSerializer
from rest_framework.views import APIView

class PatientData(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def list(self, request):
        qs = Patient.objects.all()
        patient_serializer = PatientSerializer(qs, many=True)
        return Response(patient_serializer.data, status.HTTP_200_OK)

'''class PatientVisitData(APIView):
    def get(self, request):
        try:
            patient_qs = Patient.objects.all()
            patient_serializer = PatientSerializer(patient_qs, many = True)

            visit_qs = Visit.objects.all()
            visit_serializer = VisitSerializer(visit_qs, many=True)

            return_data = {
                "patient": patient_serializer.data,
                "visit": visit_serializer.data
            }
            return Response(data = return_data, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(data={"msg": "Internal server error", "detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''        

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
    #return render(request, 'purrfectcareview/login.html')
    return render(request)


def index(request: HttpRequest):

    employee_id = request.session.get("employee_id")
    employee = Employee.objects.get(id=1)

    visits = Visit.objects.filter(visits_employee_id=employee)

    context = {
        'employee': employee,
        'visits': visits,
    }

    return render(request, 'purrfectcareview/index.html', context)

def logout_view(request: HttpRequest):
    request.session.flush()
    return render(request, 'purrfectcareview/login.html')


def patients_view(request: HttpRequest):
    
    patients = Patient.objects.all
    
    context = {
        'patients': patients
    }

    return render(request, 'purrfectcareview/patients.html', context)


def patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {'patient': patient}
    return render(request, 'purrfectcareview/patient_details.html', context)


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

