# Generated by Django 4.2.5 on 2023-12-05 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purrfectcareview', '0008_patient_patient_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='images/default_image.jpg', upload_to='images/'),
        ),
    ]
