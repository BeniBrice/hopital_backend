from django.shortcuts import render  # noqa
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny

from KiraMeeT.Response_messages import error_response, success_response
from KiraMeeT.views_mixins import MultipleSerializerAPIMixin

from .models import Doctor, Specialty
from .serializers import DoctorCreateSerializer, DoctorSerializer, DoctorUpdateSerializer, SpecialitySerializer


class SpecialtyViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Specialty.objects.all()
    serializer_class = SpecialitySerializer

    # Surcharge de la méthode `create` pour gérer les réponses
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Validation des données
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": True,
                "message": "Specialty created successfully.",
                "code": status.HTTP_201_CREATED,
                "data": serializer.data,
            }
            return success_response(
                "Specialty created successfully.",
                response_data,
                status.HTTP_201_CREATED,
            )

        # Gestion des erreurs
        return error_response(
            "Specialty creation failed.",
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )


class DoctorViewSet(MultipleSerializerAPIMixin, viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = DoctorSerializer
    create_serializer_class = DoctorCreateSerializer
    update_serializer_class = DoctorUpdateSerializer
    queryset = Doctor.objects.all()