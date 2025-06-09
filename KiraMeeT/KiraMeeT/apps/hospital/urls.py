from django.urls import path

from .views import *


urlpatterns = [
    path("hospital_list/", HospitalView.as_view(), name="hospital_list/"),
    path("specialities_list/", SpecialitiesView.as_view(), name="specialities_list/"),
]
