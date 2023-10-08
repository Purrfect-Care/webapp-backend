from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.index, name="index"),
    path("patients/", views.patients_view, name='patients_view'),
    path('patient/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('add_patient/', views.add_patient, name='add_patient'),
]