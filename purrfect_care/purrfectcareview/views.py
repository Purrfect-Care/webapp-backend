from django.http import HttpRequest, HttpResponse
from .models import Employee, Visit
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import custom_login_required

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
