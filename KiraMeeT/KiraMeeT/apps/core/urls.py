from django.urls import path

from .views import *

app_name = "core"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("create_profil/", CreateProfil.as_view(), name="create_profil"),
    path("update_profil/", UpdateProfileApiView.as_view(), name="update_profil"),
]
