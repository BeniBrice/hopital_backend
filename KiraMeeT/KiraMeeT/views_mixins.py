import logging

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied  # noqa
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

# from . import error_codes

logger = logging.getLogger(__name__)


class MultipleSerializerAPIMixin:
    serializer_class = None
    detail_serializer_class = None
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None

    def get_serializer_class(self):
        if not hasattr(self, "action"):
            return super().get_serializer_class()

        # Handling the two names of serializers (detail and details)
        if hasattr(self, "details_serializer_class"):
            self.detail_serializer_class = self.details_serializer_class

        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        elif self.action in ["update", "partial_update"] and self.update_serializer_class is not None:
            return self.update_serializer_class
        elif self.action == "create" and self.create_serializer_class is not None:
            return self.create_serializer_class
        elif self.action == "list":
            if str(self.request.query_params.get("full_object", None)).lower() == "true":
                return self.detail_serializer_class or self.list_serializer_class or self.serializer_class

            return self.list_serializer_class or self.serializer_class

        return super().get_serializer_class()