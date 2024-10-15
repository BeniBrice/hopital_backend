from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication  # noqa

# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from KiraMeeT.apps.core.models import User  # noqa
from KiraMeeT.Response_messages import error_response, success_response

from .serializers import UserLoginSerializer, UserSignupSerializer


class SignupAPIView(APIView):
    """
    API view pour la création d'un compte utilisateur.
    """

    permission_classes = []

    def post(self, request):
        try:
            # Récupérer les champs 'password' et 'confirm_password'
            password = request.data.get("password")
            confirm_password = request.data.get("confirm_password")

            if password != confirm_password:
                # Si les mots de passe ne correspondent pas, lever une exception
                raise ValidationError(
                    {"password_mismatch": "Les mots de passe ne correspondent pas."}
                )

            # Sérialiser les données du formulaire
            serializer = UserSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Enregistrer l'utilisateur si tout est valide
            serializer.save()

            # Retourner une réponse avec les données utilisateur et un statut 201
            return Response(
                {"message": "Utilisateur créé avec succès.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            # Gérer les erreurs de validation DRF
            return Response(
                {"error": "Erreur de validation", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except DjangoValidationError as e:
            # Gérer les erreurs de validation spécifiques à Django (comme les mots de passe)
            return Response(
                {
                    "error": "Erreur de validation du mot de passe",
                    "details": e.messages,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # Gérer les autres types d'erreurs (500)
            return Response(
                {"error": "Erreur interne du serveur", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    # authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        # Utiliser le serializer pour valider les données de requête
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            # Vérifier si l'utilisateur existe avec l'email et mot de passe
            user = authenticate(username=email, password=password)

            if user:
                # Générer ou obtenir un token
                token, created = Token.objects.get_or_create(user=user)

                response_data = {"email": user.email, "token": token.key}
                return success_response(
                    "User connected successfully.", response_data, status.HTTP_200_OK
                )
            else:
                return error_response(
                    "Invalid credentials, please try again.",
                    status.HTTP_401_UNAUTHORIZED,
                )

        # Si les données ne sont pas valides, retourner les erreurs de validation
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
