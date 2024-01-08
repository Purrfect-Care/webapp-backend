from .models import Employee, Visit, VisitType, VisitSubtype, Patient, Owner, Prescription, IllnessHistory, Illness, \
    Clinic, Medication, \
    PrescribedMedication, Photo, Species, Breed
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import OwnerSerializer, VisitTypeSerializer, VisitSubtypeSerializer, PatientSerializer, \
    VisitSerializer, IllnessHistorySerializer, PrescriptionSerializer, EmployeeSerializer, PatientSideBarListSerializer, \
    IllnessSerializer, ClinicSerializer, \
    MedicationSerializer, PrescribedMedicationSerializer, PhotoSerializer, SpeciesSerializer, BreedSerializer
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import jwt
from argon2 import PasswordHasher
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os
from rest_framework.response import Response
from rest_framework import status
from copy import deepcopy

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_old_photo(request, file_name):
    try:
        # Assuming your photos are stored in the media directory within the project
        file_path = os.path.join('/webapp-backend', 'purrfect_care', 'media', 'profile_pictures', file_name)

        print(f"Attempting to delete file: {file_path}")

        # Check if the file is named "default.png" and skip deletion
        if file_name == 'default.png':
            return JsonResponse({'message': 'File is named default.png and will not be deleted'})

        # Implement logic to delete the file
        if os.path.exists(file_path):
            os.remove(file_path)

            # Respond with success
            return JsonResponse({'message': 'Photo deleted successfully'}, status=204)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_empty_prescriptions(request):
    try:
        # Fetch all prescriptions
        prescriptions = Prescription.objects.all()

        # Iterate through prescriptions
        for prescription in prescriptions:
            # Check if the prescription has no attached medications
            if not prescription.prescribed_medications.exists():
                # If empty, delete the prescription
                prescription.delete()
                print('Empty prescription deleted successfully')

        return JsonResponse({'success': True, 'message': 'Empty prescriptions deleted successfully'})
    except Exception as e:
        print(f'Error deleting empty prescriptions: {str(e)}')
        return JsonResponse({'success': False, 'message': f'Error deleting empty prescriptions: {str(e)}'})


class IllnessHistoryView(viewsets.ModelViewSet):
    serializer_class = IllnessHistorySerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id', None)

        # Validate that the patient_id parameter is provided
        if patient_id is None:
            return IllnessHistory.objects.all()

        # Filter illness history by patient_id
        queryset = IllnessHistory.objects.filter(illness_history_patient_id=patient_id)
        return queryset


class PhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        visit_id = self.request.query_params.get('visit_id', None)

        if visit_id is None:
            return Photo.objects.all()

        queryset = Photo.objects.filter(photos_visit_id=visit_id)
        return queryset


class IllnessView(viewsets.ModelViewSet):
    serializer_class = IllnessSerializer
    queryset = Illness.objects.all()


class PatientView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Patient.objects.all()


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    

class OwnerView(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()


class PrescriptionsView(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id', None)

        # Validate that the patient_id parameter is provided
        if patient_id is None:
            return Prescription.objects.all()

        # Filter illness history by patient_id
        queryset = Prescription.objects.filter(prescriptions_patient_id=patient_id)
        return queryset


class VisitSubtypeView(viewsets.ModelViewSet):
    serializer_class = VisitSubtypeSerializer
    queryset = VisitSubtype.objects.all()


class VisitTypeView(viewsets.ModelViewSet):
    serializer_class = VisitTypeSerializer
    queryset = VisitType.objects.all()


class VisitView(viewsets.ModelViewSet):
    serializer_class = VisitSerializer

    def get_queryset(self):
        employee_id = self.request.query_params.get('employee_id', None)
        patient_id = self.request.query_params.get('patient_id', None)
        clinic_id = self.request.query_params.get('clinic_id', None)

        if clinic_id is not None:
            queryset = Visit.objects.filter(visits_clinic_id=clinic_id).order_by('visit_datetime')
        elif employee_id is not None:
            queryset = Visit.objects.filter(visits_employee_id=employee_id).order_by('visit_datetime')
        elif patient_id is not None:
            queryset = Visit.objects.filter(visits_patient_id=patient_id).order_by('visit_datetime')
        else:
            queryset = Visit.objects.all().order_by('visit_datetime')

        return queryset
    
    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('visits_employee_id')
        visit_datetime = request.data.get('visit_datetime')
        overlapping_visits = Visit.objects.filter(visits_employee_id=employee_id, visit_datetime=visit_datetime)
        
        if overlapping_visits.exists():
            return Response({"message": "This vet already has a visit at this time."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)


class MedicationView(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer


class PrescribedMedicationView(viewsets.ModelViewSet):
    queryset = PrescribedMedication.objects.all()
    serializer_class = PrescribedMedicationSerializer


class BreedView(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class SpeciesView(viewsets.ModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class EmployeeView(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        mutable_data = deepcopy(request.data)
        # You can perform custom logic before or after calling the super().create()
        ph = PasswordHasher()
        # Example: You may want to hash the password before saving
        raw_password = mutable_data.get('employee_password')
        hashed_password = ph.hash(raw_password)
        mutable_data['employee_password'] = hashed_password
        response = super().create(request, *args, **kwargs)
        # You can perform additional actions after the object is created
        # Example: Send a welcome email
        return response
    


    def get_queryset(self):
        employee_role = self.request.query_params.get('employee_role', None)
        employees_clinic_id = self.request.query_params.get('employees_clinic_id', None)

        if employee_role is not None and employees_clinic_id is not None:
            queryset = Employee.objects.filter(employee_role=employee_role, employees_clinic_id=employees_clinic_id)
        if employees_clinic_id is not None:
            queryset = Employee.objects.filter(employees_clinic_id=employees_clinic_id)
        else:
            queryset = Employee.objects.all()

        return queryset


class PatientSideBarListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PatientSideBarListSerializer
    queryset = Patient.objects.all()


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            ph = PasswordHasher()
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(email)
            print(password)
            user = Employee.objects.get(employee_email=email)
            if user is not None and ph.verify(user.employee_password, password):
                expiration_time = timezone.now() + timedelta(hours=2)
                user_data = {
                "id": user.id,
                "employee_role": user.employee_role,
                "employee_first_name": user.employee_first_name,
                "employee_last_name": user.employee_last_name,
                "employees_clinic_id": user.employees_clinic_id.id
                }
                token_payload = {
                    "id": user.id,
                    "employee_role": user.employee_role,
                    "employee_first_name": user.employee_first_name,
                    "employee_last_name": user.employee_last_name,
                    "employees_clinic_id": user.employees_clinic_id.id,
                    'exp': expiration_time.timestamp()
                }
                token = jwt.encode(token_payload, 'your_secret_key', algorithm='HS256')
                print(expiration_time.timestamp())
                print(datetime.fromtimestamp(expiration_time.timestamp())
)
                # Authentication successful
                return JsonResponse({'message': 'Login successful', 'token': token, 'expiration_time': int(expiration_time.timestamp()), 'employee': user_data}, content_type='application/json')
            else:
                # Authentication failed
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            return JsonResponse({'message': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


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

