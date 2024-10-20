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


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ("email", "password")

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        # Vérifier que l'email et le mot de passe sont fournis
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        # Vérifier que l'utilisateur existe avec cet email
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "No user is registered with this email address."
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "contact",
            "CNI",
        ]
