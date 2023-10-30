from rest_framework import serializers
from . import models
from datetime import date


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Species
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    breeds_species_id = SpeciesSerializer()

    def validate(self, data):
        selected_species = self.context.get('selected_species')
        if selected_species and data['breeds_species_id'] != selected_species:
            raise serializers.ValidationError("Breed species must match the selected species.")
        return data

    class Meta:
        model = models.Breed
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
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
    patients_owner_id = OwnerSerializer()
    patients_species_id = SpeciesSerializer()
    patients_breed_id = BreedSerializer()

    def validate(self, data):
        if data["patient_date_of_birth"] > date.today():
            raise serializers.ValidationError("Patient's date of birth cannot be a future date")
        return data

    class Meta:
        model = models.Patient
        fields = '__all__'


class IllnessHistorySerializer(serializers.ModelSerializer):
    illness_history_patient_id = PatientSerializer()
    illness_history_illness_id = IllnessSerializer()
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
    employees_clinic_id = ClinicSerializer()

    class Meta:
        model = models.Employee
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    visits_patient_id = PatientSerializer()
    visits_visit_type_id = VisitTypeSerializer()
    visits_visit_subtype_id = VisitSubtypeSerializer()
    visits_employee_id = EmployeeSerializer()

    class Meta:
        model = models.Visit
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photos_visit_id = VisitSerializer()

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
