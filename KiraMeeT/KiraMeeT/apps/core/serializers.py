from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "contact",
            "CNI",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.get("password")

        # Assurez-vous de vérifier le mot de passe ici si nécessaire
        if (
            validate_password(password) is None
        ):  # Assurez-vous que validate_password existe
            validated_data["password"] = make_password(password)

            # Création de l'utilisateur avec les données validées
            user = User.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                contact=validated_data["contact"],
                CNI=validated_data["CNI"],
            )
            return user
        else:
            raise serializers.ValidationError(
                "Le mot de passe ne répond pas aux critères de validation."
            )
