from .models import Employee, Visit, Illness, VisitType, VisitSubtype, Patient, Owner, Prescription, IllnessHistory
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from .serializers import OwnerSerializer, VisitTypeSerializer, VisitSubtypeSerializer, PatientSerializer, \
    VisitSerializer, IllnessHistorySerializer, IllnessSerializer, PrescriptionSerializer, EmployeeSerializer, PatientSideBarListSerializer


class IllnessHistoryView(viewsets.ModelViewSet):
    serializer_class = IllnessHistorySerializer
    queryset = IllnessHistory.objects.all()
    
class IllnessView(viewsets.ModelViewSet):
    serializer_class = IllnessSerializer
    queryset = Illness.objects.all()


class PatientView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class OwnerView(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()


class PrescriptionsView(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()


class VisitSubtypeView(viewsets.ModelViewSet):
    serializer_class = VisitSubtypeSerializer
    queryset = VisitSubtype.objects.all()


class VisitTypeView(viewsets.ModelViewSet):
    serializer_class = VisitTypeSerializer
    queryset = VisitType.objects.all()


class VisitView(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PatientSideBarListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSideBarListSerializer


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
    # return render(request, 'purrfectcareview/login.html')
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
