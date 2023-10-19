from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("illness_history", views.IllnessData, "illness_history")
router.register("patients", views.PatientData, "patients")


urlpatterns = [
    path('api/', include(router.urls)),
    path("", views.index, name="index"),
    path('prescriptions/', views.PrescriptionListCreateView.as_view(), name='prescription-list-create'),
    path("add_owner/", views.OwnerView.as_view({'post': 'create'}), name="add_owner"),
    path("add_visit_type/", views.VisitTypeView.as_view({'post': 'create'}), name="add_visit_type"),
    path("add_visit_subtype/", views.VisitSubtypeView.as_view({'post': 'create'}), name="add_visit_subtype"),
    # path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("patients/", views.patients_view, name='patients_view'),
]