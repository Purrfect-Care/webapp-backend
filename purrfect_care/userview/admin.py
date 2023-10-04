from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Species)
admin.site.register(Breed)
admin.site.register(Owner)
admin.site.register(Illness)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(IllnessHistory)
admin.site.register(Medication)
admin.site.register(VisitType)
admin.site.register(VisitSubtype)
admin.site.register(Employee)
admin.site.register(Visit)
admin.site.register(Photo)
admin.site.register(Prescription)
admin.site.register(PrescribedMedication)
