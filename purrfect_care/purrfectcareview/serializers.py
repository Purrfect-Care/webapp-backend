from rest_framework import serializers
from . import models
from datetime import date


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            not_allowed = set(exclude)
            for exclude_name in not_allowed:
                self.fields.pop(exclude_name)


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Species
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    breeds_species = SpeciesSerializer(source='breeds_species_id')

    def validate(self, data):
        selected_species = self.context.get('selected_species')
        if selected_species and data['breeds_species'] != selected_species:
            raise serializers.ValidationError("Breed species must match the selected species.")
        return data

    class Meta:
        model = models.Breed
        fields = '__all__'


class OwnerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Owner
        fields = '__all__'


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Illness
        fields = '__all__'


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clinic
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    patients_owner = OwnerSerializer(source='patients_owner_id')
    patients_species = SpeciesSerializer(source='patients_species_id')
    patients_breed = BreedSerializer(source='patients_breed_id')

    def validate(self, data):
        if data["patient_date_of_birth"] > date.today():
            raise serializers.ValidationError("Patient's date of birth cannot be a future date")
        return data

    class Meta:
        model = models.Patient
        fields = '__all__'


class PatientSideBarListSerializer(serializers.ModelSerializer):
    patients_owner = OwnerSerializer(source='patients_owner_id', fields=['owner_first_name', 'owner_last_name'])

    class Meta:
        model = models.Patient
        fields = ('id', 'patient_name', 'patients_owner')


class IllnessHistorySerializer(serializers.ModelSerializer):
    illness_history_patient = PatientSerializer('illness_history_patient_id')
    illness_history_illness = IllnessSerializer('illness_history_illness_id')

    class Meta:
        model = models.IllnessHistory
        fields = '__all__'


class VisitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VisitType
        fields = '__all__'


class VisitSubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VisitSubtype
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    employees_clinic = ClinicSerializer('employees_clinic_id')

    class Meta:
        model = models.Employee
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    visits_patient = PatientSerializer('visits_patient_id')
    visits_visit_type = VisitTypeSerializer('visits_visit_type_id')
    visits_visit_subtype = VisitSubtypeSerializer('visits_visit_subtype_id')
    visits_employee = EmployeeSerializer('visits_employee_id')

    class Meta:
        model = models.Visit
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photos_visit = VisitSerializer('photos_visit_id')

    class Meta:
        model = models.Photo
        fields = '__all__'


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medication
        fields = '__all__'


class MedicationAmountSerializer(serializers.Serializer):
    medication = MedicationSerializer()
    medication_amount = serializers.IntegerField(min_value=1)


class PrescribedMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrescribedMedication
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_medications = PrescribedMedicationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prescription
        fields = '__all__'
