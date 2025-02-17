from django.contrib import admin  # noqa

from .models import *

# Register your models here.

admin.site.register(Specialty)
# admin.site.register(WorkTimeManager)
admin.site.register(Doctor)
admin.site.register(AppointMent)
admin.site.register(Hopital)
# admin.site.register(WorkTimeManager)
