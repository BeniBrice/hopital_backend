from django.contrib.auth.hashers import make_password  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from rest_framework import serializers  # type: ignore

from .models import User, Profil


class UserSignupSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    age = serializers.IntegerField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "contact",
            "password",
            "age",
            "profile_image",
            "country",
            "city",
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
            )

            profil_data = {
                "profile_image": validated_data.get("profile_image"),
                "age": validated_data.get("age"),
                "country": validated_data.get("country"),
                "city": validated_data.get("city"),
            }
            profil = Profil.objects.create(user=user, **profil_data)

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


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profil
        fields = [
            "profile_image",
            "age",
            "country",
            "city",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        profil = Profil.objects.create(user=user, **validated_data)
        return profil
