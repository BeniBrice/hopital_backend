from rest_framework import serializers
from .models import *


class HopitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"


class SpecialiteSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Specialitie
        fields = "__all__"
