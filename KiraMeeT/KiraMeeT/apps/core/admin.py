from django.contrib import admin  # noqa


from django.contrib import admin
from .models import User, Profil


# Register your models here.
admin.site.register(User)
admin.site.register(Profil)
