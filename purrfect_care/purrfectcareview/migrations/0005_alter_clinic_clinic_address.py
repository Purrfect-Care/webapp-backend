# Generated by Django 4.2.6 on 2023-11-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purrfectcareview', '0004_alter_employee_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='clinic_address',
            field=models.CharField(max_length=255),
        ),
    ]
