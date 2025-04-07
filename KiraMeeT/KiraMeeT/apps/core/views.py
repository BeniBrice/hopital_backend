from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication  # noqa

# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password  # type: ignore

from KiraMeeT.apps.core.models import User  # noqa
from KiraMeeT.Response_messages import error_response, success_response

from .serializers import (
    UserLoginSerializer,
    UserSignupSerializer,
    ProfilSerializer,
    UserSerializer,
)


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


class UpdateProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):  # 🔄 PUT pour mise à jour complète
        return self.update_user(request)

    def patch(self, request, *args, **kwargs):  # 🔄 PATCH pour mise à jour partielle
        return self.update_user(request, partial=True)

    def update_user(
        self, request, partial=False
    ):  # Fonction pour éviter la duplication de code
        user = request.user
        data = request.data.copy()
        data.update(request.FILES)

        serializer = UserSerializer(
            user,
            data=data,  # 📌 Ici, on passe `data` et non `request.data` pour inclure les fichiers
            partial=partial,
            context={"request": request},
        )
        if "password" in data:
            data["password"] = make_password(data["password"])

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,  # ✅ Utilise 200 au lieu de 201, car c'est une mise à jour
            )

        return Response(
            {
                "success": False,
                "message": "Error while updating user",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# class UpdateProfileApiView(APIView):

#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def put(self, request, *args, **kwargs):

#         serializer = UserSignupSerializer(data=self.request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             user = User.objects.get(id=self.request.user.id)
#             if user:
#                 user_serializer = UserSerializer(user)
#                 return Response(
#                     {
#                         "success": True,
#                         "message": user_serializer.data,
#                         "status_code": status.HTTP_201_CREATED,
#                     }
#                 )
#             else:
#                 return Response(
#                     {
#                         "success": False,
#                         "message": "User not found",
#                         "status_code": status.HTTP_201_CREATED,
#                     }
#                 )

#         return Response(
#             {
#                 "success": False,
#                 "message": serializer.errors,
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#             }
#         )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    # authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        # Utiliser le serializer pour valider les données de requête
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if not password or not email:
            return Response(
                {
                    "success": False,
                    "message": "email and password is required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(
                user,
                context={"request": request},
            )

            return success_response(
                "User connected successfully.",
                serializer.data,
                status.HTTP_200_OK,
            )
        else:
            return error_response(
                "Invalid credentials, please try again.",
                status.HTTP_401_UNAUTHORIZED,
                # status.HTTP_401_UNAUTHORIZED,
                400,
            )


class CreateProfil(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfilSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profil created successfully",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED,
                }
            )
        else:
            raise ValidationError(serializer.errors)
