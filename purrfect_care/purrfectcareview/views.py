from datetime import datetime, timedelta
from .models import Employee, Visit, VisitType, VisitSubtype, Patient, Owner, Prescription, IllnessHistory, Illness
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from .serializers import OwnerSerializer, VisitTypeSerializer, VisitSubtypeSerializer, PatientSerializer, \
    VisitSerializer, IllnessHistorySerializer, PrescriptionSerializer, EmployeeSerializer, PatientSideBarListSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
import jwt

class IllnessHistoryView(viewsets.ModelViewSet):
    serializer_class = IllnessHistorySerializer
    queryset = IllnessHistory.objects.all()


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


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(email)
            print(password)

            user = Employee.objects.get(Q(employee_email=email) & Q(employee_password=password))

            if user is not None:
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