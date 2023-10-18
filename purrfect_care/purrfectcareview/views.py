
from .forms import PatientForm
from .models import Employee, Visit, Patient, Owner, Prescription, PrescribedMedication, IllnessHistory
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import OwnerSerializer, PatientSerializer, PrescribedMedicationSerializer, VisitSerializer, IllnessHistorySerializer, BreedSerializer, PrescriptionSerializer
from rest_framework.views import APIView
    
class IllnessData(viewsets.ModelViewSet):
    queryset = IllnessHistory.objects.all()
    serializer_class = IllnessHistorySerializer

    def create(self, request):
        serializer = IllnessHistorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        qs = IllnessHistory.objects.all()

        illness_serializer = IllnessHistorySerializer(qs, many=True)

        return Response(illness_serializer.data, status.HTTP_200_OK)

class PatientData(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def create(self, request):
        patient_data = request.data
        #patients_owner_id = patient_data.get('patients_owner_id')
        patient_serializer = PatientSerializer(data=request.data)
        patient_serializer.is_valid(raise_exception=True)
        patient_serializer.save()

        return Response({"msg": "Patient created"}, status=status.HTTP_201_CREATED)
    def list(self, request):
        qs = Patient.objects.all()
        patient_serializer = PatientSerializer(qs, many=True)
        return Response(patient_serializer.data, status.HTTP_200_OK)


class OwnerView(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()

    def create(self, request):
        serializer = OwnerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PrescriptionListCreateView(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def create(self, request, *args, **kwargs):
        # Validate the prescription data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create a new prescription
        self.perform_create(serializer)

        # Attach medications to the newly created prescription
        prescription = serializer.instance
        prescribed_medications_data = request.data.get('prescribed_medications', [])
        for medication_data in prescribed_medications_data:
            medication_data['prescribed_medications_prescription_id'] = prescription.id

        medication_serializer = PrescribedMedicationSerializer(data=prescribed_medications_data, many=True)
        medication_serializer.is_valid(raise_exception=True)
        medication_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            

class PrescriptionsView(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()

    def create(self, request):
        prescription_data = request.data
        existing_patient = prescription_data.get('prescriptions_patients_id')
        
        prescription_serializer = PrescriptionSerializer(data=request.data)
        prescription_serializer.is_valid(raise_exception=True)
        prescription_serializer.save()

        return Response({"msg": "Prescription created"}, status=status.HTTP_201_CREATED)






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

