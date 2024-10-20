import random
import string

from django.db import models

from KiraMeeT.apps.appointment.managers import DoctorManager
from KiraMeeT.apps.core.models import User  # noqa


class Specialty(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    longitude = models.CharField(max_length=30, blank=False, null=False)
    latitude = models.CharField(max_length=30, blank=False, null=False)
    specialite = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, null=False, blank=False
    )
    appointment_price = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    cabinet = models.CharField(max_length=100, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    objects = DoctorManager()

    def __str__(self):
        return self.cabinet


class WorkTimeTable(models.Model):
    date = models.DateField(null=False, blank=False)
    start_at = models.TimeField(null=False, blank=False)
    end_at = models.TimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class AppointMent(models.Model):
    class AppointMentStatus(models.TextChoices):
        ACCEPTED = ("AA", "Accepted")
        REFUSED = ("RE", "Refused")
        CANCELED = ("CA", "Canceled")
        WAITING = ("WA", "Waiting")

    patient = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, blank=False, null=False
    )
    appointment_time = models.ForeignKey(
        WorkTimeTable, on_delete=models.CASCADE, null=False, blank=False
    )
    appointment_number = models.CharField(max_length=20, unique=True)
    reason = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    action_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=AppointMentStatus.choices,
        default=AppointMentStatus.WAITING,
    )

    def save(self, *args, **kwargs):
        if not self.appointment_number:
            self.appointment_number = self.generate_appointment_number()
        super().save(*args, **kwargs)

    def is_accepted(self):
        self.status = AppointMent.AppointMentStatus.ACCEPTED
        self.save()
        return self.is_accepted
    
    def is_canceled(self):
        self.status = AppointMent.AppointMentStatus.CANCELED
        self.save()
        return self.is_canceled
    
    def is_refused(self):
        self.status = AppointMent.AppointMentStatus.REFUSED
        self.save()
        return self.is_refused

    def generate_appointment_number(self):
        """Generate a random unique appointment number like 'RDV-12345'."""
        digits = string.digits
        appointment_number = "RDV" + "-".join(random.choices(digits, k=5))
        return appointment_number
