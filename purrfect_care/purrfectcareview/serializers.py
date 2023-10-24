from rest_framework import serializers
from . import models
from datetime import date

class SpeciesSerializer(serializers.ModelSerializer):
    species_name = serializers.CharField(max_length=50)
    class Meta:
        model = models.Species
        fields = "__all__"

class BreedSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(max_length = 50)
    #breeds_species_id = SpeciesSerializer()
    breeds_species_id = serializers.PrimaryKeyRelatedField(queryset=models.Species.objects.all())

    def validate(self, data):
        selected_species = self.context.get('selected_species')
        if selected_species and data['breeds_species_id'] != selected_species:
            raise serializers.ValidationError("Breed species must match the selected species.")
        return data


    class Meta:
        model = models.Breed
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    owner_first_name = serializers.CharField(max_length=50)
    owner_last_name = serializers.CharField(max_length=50)
    owner_address = serializers.CharField(max_length = 255)
    owner_postcode = serializers.CharField(max_length=20)
    owner_city = serializers.CharField(max_length=50)
    owner_phone_number = serializers.CharField(max_length=50)
    owner_email = serializers.EmailField()

    class Meta:
        model = models.Owner
        fields = '__all__'

class IllnessSerializer(serializers.ModelSerializer):
    illness_name = serializers.CharField(max_length=255)
    class Meta:
        model = models.Illness
        fields = '__all__'

class ClinicSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(max_length=150)
    clinic_address = serializers.CharField(max_length=255)
    clinic_postcode = serializers.CharField(max_length=20)
    clinic_city = serializers.CharField(max_length=50)
    clinic_phone_number = serializers.CharField(max_length=20)
    clinic_email = serializers.EmailField()
    class Meta:
        model = models.Clinic
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(max_length=255)
    GENDER_CHOICES = models.Patient.GENDER_CHOICES
    patient_gender = serializers.ChoiceField(choices = GENDER_CHOICES)
    patient_date_of_birth = serializers.DateField(required = False, allow_null = True)
    patients_owner_first_name = serializers.CharField(source = 'patients_owner_id.owner_first_name')
    patients_owner_last_name = serializers.CharField(source = 'patients_owner_id.owner_last_name')
    patients_owner_address = serializers.CharField(source = 'patients_owner_id.owner_address')
    patients_owner_postcode = serializers.CharField(source = 'patients_owner_id.owner_postcode')
    patients_owner_city = serializers.CharField(source = 'patients_owner_id.owner_city')
    patients_owner_phone_number = serializers.CharField(source = 'patients_owner_id.owner_phone_number')
    patients_owner_email = serializers.CharField(source = 'patients_owner_id.owner_email')
    patients_species_name = serializers.CharField(source = 'patients_species_id.species_name')
    patients_breed_name = serializers.CharField(source = 'patients_breed_id.breed_name')


    
    def validate(self, data):
        if data["patient_date_of_birth"] > date.today():
            raise serializers.ValidationError("Patient's date of birth cannot be a future date")
        return data
    
    class Meta:
        model = models.Patient
        fields = '__all__'


class IllnessHistorySerializer(serializers.ModelSerializer):
    illness_history_patient_name = serializers.CharField(source = 'illness_history_patient_id.patient_name')
    illness_history_illness_name = serializers.CharField(source = 'illness_history_illness_id.illness_name')
    illness_onset_date = serializers.DateField()

    class Meta:
        model = models.IllnessHistory
        fields = '__all__'



class VisitTypeSerializer(serializers.ModelSerializer):
    visit_type_name = serializers.CharField(max_length=100)
    class Meta:
        model = models.VisitType
        fields = '__all__'

class VisitSubtypeSerializer(serializers.ModelSerializer):
    visit_subtype_name = serializers.CharField(max_length=100)
    visit_subtypes_visit_type_id = serializers.PrimaryKeyRelatedField(
        queryset=models.VisitType.objects.all())
    class Meta:
        model = models.VisitSubtype
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    employee_role = serializers.CharField(max_length=100)
    employee_first_name = serializers.CharField(max_length=50)
    employee_last_name = serializers.CharField(max_length=50)
    employee_address = serializers.CharField(max_length=255)
    employee_postcode = serializers.CharField(max_length=20)
    employee_city = serializers.CharField(max_length=50)
    employee_phone_number = serializers.CharField(max_length=20)
    employee_email = serializers.EmailField()
    employee_password = serializers.CharField(max_length=64)
    employees_clinic_id = ClinicSerializer()

    class Meta:
        model = models.Employee
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    visit_datetime = serializers.DateTimeField(default=date.today)
    visit_duration = serializers.TimeField()
    visits_patient_id = PatientSerializer()
    visits_visit_type_id = VisitTypeSerializer()
    visits_visit_subtype_id = VisitSubtypeSerializer()
    visits_employee_id = EmployeeSerializer()
    VISIT_STATUS_CHOICES = models.Visit.VISIT_STATUS_CHOICES
    visit_status = serializers.ChoiceField(choices=VISIT_STATUS_CHOICES)
    visit_description = serializers.CharField(required = False, allow_null = True)
    patient_weight = serializers.DecimalField(max_digits=5, decimal_places=2, required = False, allow_null = True)
    patient_height = serializers.DecimalField(max_digits=5, decimal_places=2, required = False, allow_null = True)

    class Meta:
        model = models.Visit
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    photo_name = serializers.CharField(max_length=255)
    photos_visit_id = VisitSerializer()
    photo_description = serializers.CharField(required = False, allow_null = True)

    class Meta:
        model = models.Photo
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # Assuming the medication model has an 'id' field
    medication_name = serializers.CharField(max_length=255)
    class Meta:
        model = models.Medication
        fields = '__all__'

class MedicationAmountSerializer(serializers.Serializer):
    medication = MedicationSerializer()  # Assuming you have a MedicationSerializer
    medication_amount = serializers.IntegerField(min_value=1)

    

class PrescribedMedicationSerializer(serializers.ModelSerializer):
    prescribed_medications_prescription_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Prescription.objects.all()
    )
    medication_name = serializers.CharField(source='prescribed_medications_medication_id.medication_name')
    medication_amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = models.PrescribedMedication
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='prescriptions_patient_id.patient_name')
    prescription_date = serializers.DateField(default=date.today)
    prescribed_medications = PrescribedMedicationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prescription
        fields = '__all__'      

