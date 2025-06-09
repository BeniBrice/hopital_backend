import logging
from KiraMeeT import Response_messages
from rest_framework import status
from .serializer import *
from .models import *
from rest_framework.generics import ListAPIView
from KiraMeeT.mixins import ListCustomPaginationMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)


class HospitalView(ListCustomPaginationMixin, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HopitalListSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Hospital.objects.all().order_by("-name")
        return queryset


class SpecialitiesView(ListCustomPaginationMixin, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialiteSerialiser
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Specialitie.objects.all().order_by("name")
        return queryset
