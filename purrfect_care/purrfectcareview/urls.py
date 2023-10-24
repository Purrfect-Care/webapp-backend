from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers

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


urlpatterns = [
    path('api/', include(router.urls)),
    path("", views.index, name="index"),
    # path("login/", views.login_view, name="login"),
    # path("logout/", views.logout_view, name="logout"),
]