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
    patients_owner = OwnerSerializer(source='patients_owner_id', read_only=True)
    patients_species = SpeciesSerializer(source='patients_species_id', read_only=True)
    patients_breed = BreedSerializer(source='patients_breed_id', read_only=True)

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
    illness_history_patient = PatientSerializer(source='illness_history_patient_id')
    illness_history_illness = IllnessSerializer(source='illness_history_illness_id')

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
    employees_clinic = ClinicSerializer(source='employees_clinic_id', read_only=True)

    class Meta:
        model = models.Employee
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    visits_patient = PatientSerializer(source='visits_patient_id', read_only=True)
    visits_visit_type = VisitTypeSerializer(source='visits_visit_type_id', read_only=True)
    visits_visit_subtype = VisitSubtypeSerializer(source='visits_visit_subtype_id', read_only=True)
    visits_employee = EmployeeSerializer(source='visits_employee_id', read_only=True)

    class Meta:
        model = models.Visit
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.visit_datetime = validated_data.get('visit_datetime', instance.visit_datetime)
        instance.visit_duration = validated_data.get('visit_duration', instance.visit_duration)
        instance.visit_status = validated_data.get('visit_status', instance.visit_status)
        instance.visit_description = validated_data.get('visit_description', instance.visit_description)
        instance.patient_weight = validated_data.get('patient_weight', instance.patient_weight)
        instance.patient_height = validated_data.get('patient_height', instance.patient_height)

        # Update related fields if provided in validated data
        visits_employee_id = validated_data.get('visits_employee_id')
        if visits_employee_id is not None:
            instance.visits_employee_id = visits_employee_id

        visits_visit_type_id = validated_data.get('visits_visit_type_id')
        if visits_visit_type_id is not None:
            instance.visits_visit_type_id = visits_visit_type_id

        visits_visit_subtype_id = validated_data.get('visits_visit_subtype_id')
        if visits_visit_subtype_id is not None:
            instance.visits_visit_subtype_id = visits_visit_subtype_id

        instance.save()

        return instance

class PhotoSerializer(serializers.ModelSerializer):
    photos_visit = VisitSerializer(source='photos_visit_id')

    class Meta:
        model = models.Photo
        fields = '__all__'


class MedicationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = models.Medication
        fields = '__all__'


class MedicationAmountSerializer(serializers.Serializer):
    medication = MedicationSerializer()
    medication_amount = serializers.IntegerField(min_value=1)


class PrescribedMedicationSerializer(serializers.ModelSerializer):
    medication_name = MedicationSerializer(source = 'prescribed_medications_medication_id', fields=['medication_name'])
    class Meta:
        model = models.PrescribedMedication
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_medications = PrescribedMedicationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Prescription
        fields = '__all__'
