import random
import string

from django.db import models

from KiraMeeT.apps.appointment.managers import DoctorManager, WorkTimeManager  # type: ignore
from KiraMeeT.apps.core.models import User  # type: ignore # noqa


class Specialty(models.Model):
    class speciality_choices(models.TextChoices):
        ANESTHESILOGIE = ("ANE", "Anesthésiologie")
        CARDIOLOGIE = ("CAR", "Cardiologie")
        DERMATOLOGIE = ("DERM", "Dermatologie")
        ENDOCRINOLOGIE = ("ENDO", "Endocrinologie")
        GASTRO_ENTEROLOGIE = ("GA_EN", "Gastro-entérologie")
        GENETIQUE_MEDICALE = ("GE_ME", "Génétique médicale")
        GERIATRIE = ("GER", "Gériatrie")
        HEMATOLOGIE = ("HE", "Hématologie")
        IMMUNOLOGIE = ("IMM", "Immunologie")
        NEPHROLOGIE = ("NEP", "Néphrologie")
        NEUROLOGIE = ("NEU", "Neurologie")
        ONCOLOGIE = ("ONC", "Oncologie")
        PEDIATRIE = ("PE", "Pédiatrie")
        PHYSIATRIE = ("PHY", "Physiatrie")
        PNEUMOLOGIE = ("PNEU", "Pneumologie")
        PSYCHIATRIE = ("PSY", "psychiatrie")
        RHUMATOLOGIE = ("RHU", "Rhumatologie")

    speciality_list = [
        speciality_choices.choices,
        # ANESTHESILOGIE,
        # CARDIOLOGIE,
        # DERMATOLOGIE,
        # ENDOCRINOLOGIE,
        # GASTRO_ENTEROLOGIE,
        # GENETIQUE_MEDICALE,
        # GERIATRIE,
        # HEMATOLOGIE,
        # IMMUNOLOGIE,
        # NEPHROLOGIE,
        # NEUROLOGIE,
        # ONCOLOGIE,
        # PEDIATRIE,
        # PHYSIATRIE,
        # PNEUMOLOGIE,
        # PHYSIATRIE,
        # RHUMATOLOGIE,
    ]

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        choices=speciality_choices.choices,
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# this model represents hopital model
class Hopital(models.Model):
    name = models.CharField(max_length=250, blank=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    city = models.CharField(max_length=250, blank=False, null=False)
    country = models.CharField(max_length=250, blank=False, null=False)
    phone_number = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    website = models.URLField(blank=False, null=False)
    description = models.TextField(null=False, blank=False)
    logo = models.ImageField(upload_to="hopital_logo/", blank=True, null=True)
    created_at = created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "hopital"
        verbose_name_plural = "hopitals"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hopital = models.ForeignKey(
        Hopital, on_delete=models.CASCADE, blank=True, null=True
    )
    longitude = models.CharField(max_length=30, blank=False, null=True)
    latitude = models.CharField(max_length=30, blank=False, null=True)
    specialite = models.ManyToManyField(Specialty, related_name="doctors")
    appointment_price = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    rating = models.FloatField(default=0.0)
    cabinet = models.CharField(max_length=100, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = DoctorManager()

    def __str__(self):
        return self.cabinet


class WorkTimeTable(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, null=False, blank=False
    )
    date = models.DateField(null=False, blank=False)
    start_at = models.TimeField(null=False, blank=False)
    end_at = models.TimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # objects = WorkTimeManager()

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
        return self.status

    def is_refused(self):
        self.status = AppointMent.AppointMentStatus.REFUSED
        self.save()
        return self.status

    def generate_appointment_number(self):
        """Generate a random unique appointment number like 'RDV-12345'."""
        digits = string.digits
        appointment_number = "RDV" + "-".join(random.choices(digits, k=5))
        return appointment_number
