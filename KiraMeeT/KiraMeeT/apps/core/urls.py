from django.urls import path

from .views import SignupAPIView

app_name = "core"  # Utilisation d'un espace de noms

urlpatterns = [
    path(
        "signup/", SignupAPIView.as_view(), name="signup"
    ),  # Ajoute l'endpoint pour le signup
]
