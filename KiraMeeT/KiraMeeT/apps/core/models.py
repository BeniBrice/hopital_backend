from django.contrib.auth.models import (  # Group,; Permission,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


from KiraMeeT.apps.core.managers import CustomUserManager
from KiraMeeT.apps.hospital.models import *
from KiraMeeT.models_utils import ModelsUtils


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    contact = models.CharField(
        blank=False,
        null=True,
        max_length=250,
    )
    # groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    # user_permissions = models.ManyToManyField(
    #     Permission, related_name="custom_users", blank=True
    # )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_admin(self):
        return self.is_superuser and self.is_staff

    def deactivate_user(self):
        self.is_active = False
        self.save()
        return True

    def activate_user(self):
        self.is_active = True
        self.save()
        return True


class Profil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil",
    )
    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="profile_photos/",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    is_doctor = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender=User)
    # def create_auth_token(sender, instance, created, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)


class Doctor(models.Model):
    CURRENCY_CHOICE = [
        ("bif", "Bif"),
        ("usd", "Usd"),
        ("eur", "Eur"),
    ]
    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("suspended", "Suspended"),
        ("refused", "Refused"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctors",
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors",
    )
    specialitie = models.ForeignKey(
        Specialitie,
        on_delete=models.CASCADE,
        related_name="doctors",
    )
    appointement_price = models.FloatField(
        blank=True,
        null=False,
        default=0,
    )
    rating = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    bio = models.TextField(
        blank=False,
        null=False,
    )
    status = models.CharField(
        default="pending",
        choices=STATUS,
    )
    price_currency = models.CharField(
        max_length=250, blank=True, default="bif", choices=CURRENCY_CHOICE
    )

    availability = models.JSONField(
        null=False,
        blank=False,
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        default=0,
    )
    is_actif = models.BooleanField(
        default=False,
    )
    created_at = ModelsUtils.datetime_model_field()
    updated_at = ModelsUtils.datetime_model_field()
