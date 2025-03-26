from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, UserDetailsView, LogoutView, CSRFTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("register/verify/", VerifyOTPView.as_view(), name="verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", UserDetailsView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("csrf/", CSRFTokenView.as_view(), name="csrf"),
]
