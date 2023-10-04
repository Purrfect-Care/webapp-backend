# Generated by Django 4.2.5 on 2023-10-04 15:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=150, unique=True)),
                ('clinic_address', models.CharField(max_length=255, unique=True)),
                ('clinic_postcode', models.CharField(max_length=20)),
                ('clinic_city', models.CharField(max_length=50)),
                ('clinic_phone_number', models.CharField(max_length=20, unique=True)),
                ('clinic_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_role', models.CharField(max_length=100)),
                ('employee_first_name', models.CharField(max_length=50)),
                ('employee_last_name', models.CharField(max_length=50)),
                ('employee_address', models.CharField(max_length=255)),
                ('employee_postcode', models.CharField(max_length=20)),
                ('employee_city', models.CharField(max_length=50)),
                ('employee_phone_number', models.CharField(max_length=20, unique=True)),
                ('employee_email', models.EmailField(max_length=254, unique=True)),
                ('employee_password', models.CharField(max_length=64)),
                ('employees_clinic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illness_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_first_name', models.CharField(max_length=50)),
                ('owner_last_name', models.CharField(max_length=50)),
                ('owner_address', models.CharField(max_length=255)),
                ('owner_postcode', models.CharField(max_length=20)),
                ('owner_city', models.CharField(max_length=50)),
                ('owner_phone_number', models.CharField(max_length=20, unique=True)),
                ('owner_email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=255)),
                ('patient_gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('patient_date_of_birth', models.DateField(blank=True, null=True)),
                ('patients_breed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.breed')),
                ('patients_owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_type_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisitSubtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_subtype_name', models.CharField(max_length=100, unique=True)),
                ('visit_subtypes_visit_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.visittype')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_datetime', models.DateTimeField()),
                ('visit_duration', models.TimeField()),
                ('visit_status', models.CharField(choices=[('planned', 'Planned'), ('cancelled', 'Cancelled'), ('complete', 'Complete')], max_length=10)),
                ('visit_description', models.TextField(blank=True, null=True)),
                ('patient_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('patient_height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('visits_employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.employee')),
                ('visits_patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.patient')),
                ('visits_visit_subtype_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.visitsubtype')),
                ('visits_visit_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.visittype')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription_date', models.DateField(default=django.utils.timezone.now)),
                ('prescriptions_patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.patient')),
            ],
        ),
        migrations.CreateModel(
            name='PrescribedMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_amount', models.PositiveIntegerField()),
                ('prescribed_medications_medication_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.medication')),
                ('prescribed_medications_prescription_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_name', models.CharField(max_length=255)),
                ('photo_description', models.TextField(blank=True, null=True)),
                ('photos_visit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.visit')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='patients_species_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.species'),
        ),
        migrations.CreateModel(
            name='IllnessHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illness_onset_date', models.DateField()),
                ('illness_history_illness_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.illness')),
                ('illness_history_patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.patient')),
            ],
        ),
        migrations.AddField(
            model_name='breed',
            name='breeds_species_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purrfectcareview.species'),
        ),
    ]
