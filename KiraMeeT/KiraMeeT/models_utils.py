from django.db import models
from django.utils import timezone


class ModelsUtils:
    @staticmethod
    def datetime_model_field():
        return models.DateTimeField(default=timezone.now)
