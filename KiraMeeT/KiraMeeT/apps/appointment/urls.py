from rest_framework import routers

from KiraMeeT.apps.appointment.views import (
    AppointMentViewset,
    DoctorViewSet,
    SpecialtyViewset,
    WorkTimeTAbleViewSet,
)

app_name = "appointment"

router = routers.DefaultRouter()

router.register(r"specialite", SpecialtyViewset, basename="specialite_api")
router.register(r"doctor", DoctorViewSet, basename="doctor_api")
router.register(r"workingTime", WorkTimeTAbleViewSet, basename="working_time")
router.register(r"appointment", AppointMentViewset, basename="appointment_api")


urlpatterns = router.urls
