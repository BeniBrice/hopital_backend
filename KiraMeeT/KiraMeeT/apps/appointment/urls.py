from rest_framework import routers

from KiraMeeT.apps.appointment.views import DoctorViewSet, SpecialtyViewset

app_name = "appointment"

router = routers.DefaultRouter()

router.register(r"specialite", SpecialtyViewset, basename="specialite_api")
router.register(r"doctor", DoctorViewSet, basename="doctor_api")


urlpatterns = router.urls
