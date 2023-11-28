from .models import Employee, Visit, VisitType, VisitSubtype, Patient, Owner, Prescription, IllnessHistory, Illness, Clinic
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import OwnerSerializer, VisitTypeSerializer, VisitSubtypeSerializer, PatientSerializer, \
    VisitSerializer, IllnessHistorySerializer, PrescriptionSerializer, EmployeeSerializer, PatientSideBarListSerializer, IllnessSerializer, ClinicSerializer
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import jwt
from argon2 import PasswordHasher

class IllnessHistoryView(viewsets.ModelViewSet):
    serializer_class = IllnessHistorySerializer
    queryset = IllnessHistory.objects.all()
    
class IllnessView(viewsets.ModelViewSet):
    serializer_class = IllnessSerializer
    queryset = Illness.objects.all()


class PatientView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
    

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
                    'user_id': user.id,
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
