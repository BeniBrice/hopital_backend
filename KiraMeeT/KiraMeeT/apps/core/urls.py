from django.urls import path

from .views import LoginAPIView, SignupAPIView

app_name = "core"

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("signup/", SignupAPIView.as_view(), name="signup"),
]
