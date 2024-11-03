from rest_framework import serializers

from KiraMeeT.apps.appointment.models import (
    AppointMent,
    Doctor,
    Specialty,
    WorkTimeTable,
)
from KiraMeeT.apps.core.serializers import UserSerializer


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = "__all__"

    def create(self, validated_data):
        specialty = Specialty.objects.create(**validated_data)
        return specialty


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialite = SpecialitySerializer()

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "longitude",
            "latitude",
            "specialite",
            "appointment_price",
            "address",
            "cabinet",
        ]


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "longitude",
            "latitude",
            "specialite",
            "appointment_price",
            "address",
            "cabinet",
        ]

    def create_doctor(self, validated_data):
        doctor = Doctor.objects.create_doctor(**validated_data)
        return doctor


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "user",
            "longitude",
            "latitude",
            "specialite",
            "appointment_price",
            "address",
            "cabinet",
        ]


class WorkTimeTableSerializer(serializers.ModelSerializer):
    doctor = DoctorCreateSerializer()

    class Meta:
        model = WorkTimeTable
        fields = ["id", "doctor", "date", "start_at", "end_at"]


class WorkTimeCreateTableSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = WorkTimeTable
        fields = ["doctor", "date", "start_at", "end_at"]

    def create(self, validated_data):
        # Extract the doctor ID from validated_data
        doctor_id = validated_data.pop("doctor").id
        working = WorkTimeTable.objects.create_work_time(
            doctor=doctor_id, **validated_data
        )
        return working


class WorkTimeUpdateTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTimeTable
        fields = ["doctor", "date", "start_at", "end_at"]


class AppointMentSerializer(serializers.ModelSerializer):  # Correction du nom
    class Meta:
        model = AppointMent
        fields = [
            "patient",
            "doctor",
            "appointment_time",
            "appointment_number",
            "reason",
            "description",
        ]


class AppointMentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointMent
        fields = [
            "patient",
            "doctor",
            "appointment_time",
            "appointment_number",
            "reason",
            "description",
        ]


class AppointMentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointMent
        fields = [
            "patient",
            "doctor",
            "appointment_time",
            "appointment_number",
            "reason",
            "description",
        ]
