# import logging

# from django.shortcuts import render  # noqa
# from rest_framework import status, viewsets
# from rest_framework.permissions import AllowAny

# from KiraMeeT.Response_messages import error_response, success_response
# from KiraMeeT.views_mixins import MultipleSerializerAPIMixin

# from .models import Doctor, Specialty, WorkTimeTable
# from .serializers import (
#     DoctorCreateSerializer,
#     DoctorSerializer,
#     DoctorUpdateSerializer,
#     SpecialitySerializer,
#     WorkTimeCreateTableSerializer,
#     WorkTimeTableSerializer,
#     WorkTimeUpdateTableSerializer,
# )

# logger = logging.getLogger(__name__)


# class SpecialtyViewset(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     queryset = Specialty.objects.all()
#     serializer_class = SpecialitySerializer

#     # Surcharge de la méthode `create` pour gérer les réponses
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         # Validation des données
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {
#                 "status": True,
#                 "message": "Specialty created successfully.",
#                 "code": status.HTTP_201_CREATED,
#                 "data": serializer.data,
#             }
#             return success_response(
#                 "Specialty created successfully.",
#                 response_data,
#                 status.HTTP_201_CREATED,
#             )

#         # Gestion des erreurs
#         return error_response(
#             "Specialty creation failed.",
#             serializer.errors,
#             status.HTTP_400_BAD_REQUEST,
#         )


# class DoctorViewSet(MultipleSerializerAPIMixin, viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     serializer_class = DoctorSerializer
#     create_serializer_class = DoctorCreateSerializer
#     update_serializer_class = DoctorUpdateSerializer
#     queryset = Doctor.objects.all()


# # class WorkTimeTAbleViewSet(viewsets.ModelViewSet, MultipleSerializerAPIMixin):
# #     permission_classes = [AllowAny]
# #     print("**************")
# # serializer_class = WorkTimeTableSerializer
# # create_serializer_class = WorkTimeCreateTableSerializer
# # update_serializer_class = WorkTimeUpdateTableSerializer
# #     queryset = WorkTimeTable.objects.all()


# class WorkTimeTAbleViewSet(viewsets.ModelViewSet, MultipleSerializerAPIMixin):
#     permission_classes = [AllowAny]
#     queryset = WorkTimeTable.objects.all()
#     serializer_class = WorkTimeTableSerializer  # Default serializer class

#     # Specify serializers for different actions
#     create_serializer_class = WorkTimeCreateTableSerializer
#     update_serializer_class = WorkTimeUpdateTableSerializer

#     def get_serializer_class(self):
#         # Use different serializers for create and update actions
#         if self.action == "create" and hasattr(self, "create_serializer_class"):
#             return self.create_serializer_class
#         elif self.action == "update" and hasattr(self, "update_serializer_class"):
#             return self.update_serializer_class
#         return super().get_serializer_class()

#     def create(self, request, *args, **kwargs):
#         # Log the incoming data
#         # logger.debug(f"Request data: {request.data}")
#         # print("Request data:", request.data)  # For quick debugging

#         # Use the serializer selected by get_serializer_class
#         serializer = self.get_serializer(data=request.data)

#         # Validate data
#         if serializer.is_valid():
#             self.perform_create(serializer)  # Use perform_create for better modularity
#             response_data = {
#                 "status": True,
#                 "message": "Work time entry created successfully.",
#                 "code": status.HTTP_201_CREATED,
#                 "data": serializer.data,
#             }
#             return success_response(
#                 "Work time entry created successfully.",
#                 response_data,
#                 status.HTTP_201_CREATED,
#             )

#         # Handle errors
#         return error_response(
#             "Work time entry creation failed.",
#             serializer.errors,
#             status.HTTP_400_BAD_REQUEST,
#         )


# # def perform_create(self, serializer):
# #     # Add custom logic here
# #     # For example, set the current user as the creator
# #     serializer.save(created_by=self.request.user)
