from django.urls import include, path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_old_photo, delete_empty_prescriptions

router = routers.DefaultRouter()
router.register("illness_history", views.IllnessHistoryView, "illness_history")
router.register("patients", views.PatientView, "patients")
router.register("owners", views.OwnerView, "owners")
router.register("prescriptions", views.PrescriptionsView, "prescriptions")
router.register("employees", views.EmployeeView, "employees")
router.register("visit_types", views.VisitTypeView, "visit_types")
router.register("visit_subtypes", views.VisitSubtypeView, "visit_subtypes")
router.register("visits", views.VisitView, "visits")
router.register("employees", views.EmployeeView, "employees")
router.register("patients_sidebar_list", views.PatientSideBarListViewSet, "patients_sidebar_list")
router.register("illnesses", views.IllnessView, "illnesses")
router.register("clinics", views.ClinicViewSet, "clinics")
router.register("medications", views.MedicationView, "medications")
router.register("prescribedmed", views.PrescribedMedicationView, "prescribedmed")
router.register("photos", views.PhotoView, "photos")
router.register("species", views.SpeciesView, "species")
router.register("breeds", views.BreedView, "breeds")
router.register("visit_list", views.VisitListView, "visit_list")
urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.login, name='login'),
    path('delete_old_photo/<str:file_name>/', delete_old_photo, name='delete_old_photo'),
    path("empty_prescriptions/", delete_empty_prescriptions, name="empty_prescription")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)