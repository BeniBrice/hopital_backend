from django.contrib.auth.hashers import make_password  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from rest_framework import serializers  # type: ignore
from rest_framework.response import Response
from .models import User, Profil
from rest_framework import status
from KiraMeeT.fields import AbsoluteURLImageField
import logging

logger = logging.getLogger(__name__)


class UserSignupSerializer(serializers.ModelSerializer):
    profile_image = AbsoluteURLImageField(required=False)
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
                "profile_image": validated_data.get("profile_image", None),
                "age": validated_data.get(
                    "age",
                    None,
                ),
                "country": validated_data.get("country", None),
                "city": validated_data.get("city", None),
            }
            profil = Profil.objects.create(user=user, **profil_data)

            return user
        else:
            raise serializers.ValidationError(
                "Le mot de passe ne répond pas aux critères de validation."
            )

    def update(self, instance, validated_data):
        # "first_name",
        #     "last_name",
        #     "username",
        #     "email",
        #     "contact",
        #     "password",
        #     "age",
        #     "profile_image",
        #     "country",
        #     "city",

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.contact = validated_data.get("contact", instance.contact)

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()

        try:
            profil = Profil.objects.get(user=instance)
        except Profil.DoesNotExist:
            logger.error("Profil does not exist")
            return Response(
                {
                    "message": "profil not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        age = validated_data.get("age", None)
        profile_image = validated_data.get("profile_image", None)
        country = validated_data.get("country", None)
        city = validated_data.get("city", None)
        if age is not None:
            profil.age = age
        if profile_image is not None:
            profil.profile_image = profile_image
        if country is not None:
            profil.country = country
        if city is not None:
            profil.city = city

        profil.save()
        return instance

    def delete(self, instance):
        try:
            profil = Profil.objects.get(user=instance)
            profil.delete()
        except Profil.DoesNotExist:
            logger.error("Profil not found")
            return Response(
                {
                    "message": "profil not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.delete()
        return Response(
            {"message": f"L'utilisateur {instance.email} has been deleted successfuly"},
            status=status.HTTP_204_NO_CONTENT,
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


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profil
        fields = [
            "profile_image",
            "age",
            "country",
            "city",
            "is_doctor",
        ]


class UserSerializer(serializers.ModelSerializer):
    profil = ProfilSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "contact",
            "password",
            "is_staff",
            "profil",
        ]

    def update(self, instance, validated_data):
        profil_data = validated_data.pop("profil", None)
        for (
            attr,
            value,
        ) in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if profil_data:
            profil_instance = instance.profil
            for attr, value in profil_data.items():
                setattr(profil_instance, attr, value)

            profil_instance.save()

        return instance
