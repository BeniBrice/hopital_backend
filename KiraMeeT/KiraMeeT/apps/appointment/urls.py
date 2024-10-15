from rest_framework import routers

from KiraMeeT.apps.appointment.views import SpecialtyViewset

app_name = "appointment"

router = routers.DefaultRouter()

router.register(r"specialite", SpecialtyViewset)


urlpatterns = router.urls
