from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def upload_to_profile_pictures(instance, filename):
    return 'profile_pictures/{filename}'.format(filename=filename)




class Species(models.Model):
    species_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.species_name

class Breed(models.Model):
    breed_name = models.CharField(max_length=50)
    breeds_species_id = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self):
        return self.breed_name

class Owner(models.Model):
    owner_first_name = models.CharField(max_length=50)
    owner_last_name = models.CharField(max_length=50)
    owner_address = models.CharField(max_length=255)
    owner_postcode = models.CharField(max_length=20)
    owner_city = models.CharField(max_length=50)
    owner_phone_number = models.CharField(max_length=20, unique=True)
    owner_email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.owner_first_name} {self.owner_last_name}"


class Illness(models.Model):
    illness_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.illness_name


class Clinic(models.Model):
    clinic_name = models.CharField(max_length=150, unique=True)
    clinic_address = models.CharField(max_length=255)
    clinic_postcode = models.CharField(max_length=20)
    clinic_city = models.CharField(max_length=50)
    clinic_phone_number = models.CharField(max_length=20, unique=True)
    clinic_email = models.EmailField(unique=True)

    def __str__(self):
        return self.clinic_name


class Patient(models.Model):
    patient_name = models.CharField(max_length=255)
    GENDER_CHOICES = [('samiec', 'Samiec'), ('samica', 'Samica')]
    patient_gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    patient_date_of_birth = models.DateField(null=True, blank=True)
    patient_photo = models.ImageField(_("Image"), upload_to=upload_to_profile_pictures, default='profile_pictures/default.png')
    patients_owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    patients_species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
    patients_breed_id = models.ForeignKey(Breed, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_name


class IllnessHistory(models.Model):
    illness_history_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    illness_history_illness_id = models.ForeignKey(Illness, on_delete=models.CASCADE)
    illness_onset_date = models.DateField()


class Medication(models.Model):
    medication_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.medication_name


class VisitType(models.Model):
    visit_type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.visit_type_name


class VisitSubtype(models.Model):
    visit_subtype_name = models.CharField(max_length=100, unique=True)
    visit_subtypes_visit_type_id = models.ForeignKey(VisitType, on_delete=models.CASCADE)

    def __str__(self):
        return self.visit_subtype_name


class Employee(models.Model):
    employee_role = models.CharField(max_length=100)
    employee_first_name = models.CharField(max_length=50)
    employee_last_name = models.CharField(max_length=50)
    employee_address = models.CharField(max_length=255)
    employee_postcode = models.CharField(max_length=20)
    employee_city = models.CharField(max_length=50)
    employee_phone_number = models.CharField(max_length=20, unique=True)
    employee_email = models.EmailField(unique=True)
    employee_password = models.CharField(max_length=200)
    employees_clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.employee_first_name} {self.employee_last_name}"

class Visit(models.Model):
    visit_datetime = models.DateTimeField()
    visit_duration = models.TimeField()
    visits_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visits_visit_type_id = models.ForeignKey(VisitType, on_delete=models.CASCADE)
    visits_visit_subtype_id = models.ForeignKey(VisitSubtype, on_delete=models.CASCADE)
    visits_employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    VISIT_STATUS_CHOICES = [('Zaplanowana', 'zaplanowana'), ('Odwołana', 'odwołana'), ('Zakończona', 'zakończona')]
    visit_status = models.CharField(max_length=30, choices=VISIT_STATUS_CHOICES)
    visit_description = models.TextField(null=True, blank=True)
    patient_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    patient_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    visits_clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, default=1)

class Photo(models.Model):
    photos_visit_id = models.ForeignKey(Visit, on_delete=models.CASCADE)
    photo_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', default='images/default_image.jpg')

    def __str__(self):
        return self.image


class Prescription(models.Model):
    prescriptions_patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    prescriptions_employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    prescription_date = models.DateField(default=timezone.now)


class PrescribedMedication(models.Model):
    prescribed_medications_prescription_id = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='prescribed_medications')
    prescribed_medications_medication_id = models.ForeignKey(Medication, on_delete=models.CASCADE)
    medication_amount = models.PositiveIntegerField()
    medication_dosage = models.TextField(null=True, blank=True)