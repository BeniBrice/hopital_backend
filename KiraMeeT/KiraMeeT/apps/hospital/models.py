from django.db import models
from KiraMeeT.models_utils import ModelsUtils


class Hospital(models.Model):
    # status = [
    #     ("active", "Active"),
    #     ("active", "Active"),
    # ]
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        max_length=250,
        null=False,
        blank=False,
    )
    web_site = models.URLField(
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=250,
        blank=False,
        null=False,
    )
    adress = models.CharField(
        max_length=250,
        blank=False,
        null=False,
    )
    country = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    number_of_doctors = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
    )
    phone_number = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    longitude = models.FloatField(
        blank=False,
        null=False,
        default=0,
    )
    latitude = models.FloatField(
        null=False,
        blank=False,
        default=0,
    )
    is_actif = models.BooleanField(
        default=False,
    )
    logo = models.ImageField(upload_to="hopital_logo/", blank=True, null=True)

    created_at = ModelsUtils.datetime_model_field()
    updated_at = ModelsUtils.datetime_model_field()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hospital"
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"


class Specialitie(models.Model):
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    created_at = ModelsUtils.datetime_model_field()
    updated_at = ModelsUtils.datetime_model_field()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "specialitie"
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
