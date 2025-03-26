import random
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

# Utility function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Registration API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            user.otp = otp
            user.save()

            # Send OTP via email (Replace with actual email logic)
            send_mail("Your OTP", f"Your OTP is {otp}", "admin@example.com", [user.email])

            return Response({"message": "OTP sent to email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP Verification API
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email, otp=otp)
            user.is_verified = True
            user.otp = None
            user.save()
            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid OTP or user not found."}, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)

            # Generate a secure token
            token = default_token_generator.make_token(user)

            response = Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            response.set_cookie("auth_token", token, httponly=True, secure=True, samesite="Lax")

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve Logged-in User Details
class UserDetailsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
# Logout API
class LogoutView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        logout(request)
        response = Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie("auth_token")
        return response
# CSRF Token API
class CSRFTokenView(APIView):
    def get(self, request):
        return JsonResponse({"csrftoken": get_token(request)})
