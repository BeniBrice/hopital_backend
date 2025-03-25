from django.contrib.auth.models import (  # Group,; Permission,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from KiraMeeT.apps.core.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    contact = models.IntegerField(blank=False, null=True)
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

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender=User)
    # def create_auth_token(sender, instance, created, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)
