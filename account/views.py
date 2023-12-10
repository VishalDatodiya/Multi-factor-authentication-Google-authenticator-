
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login

from rest_framework import views, status
from rest_framework.response import Response
from .models import OTPSecret
from .serializers import OTPSecretSerializer
import pyotp


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class OTPVerificationView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate and send OTP secret to the client
        user = self.request.user
        if not OTPSecret.objects.filter(user=user).exists():
            secret_key = pyotp.random_base32()
            OTPSecret.objects.create(user=user, secret_key=secret_key)
        else:
            secret_key = OTPSecret.objects.get(user=user).secret_key

        totp = pyotp.TOTP(secret_key)
        otp_url = totp.provisioning_uri(name=user.username, issuer_name='google')

        return Response({'otp_url': otp_url}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify OTP
        user = self.request.user
        secret_key = OTPSecret.objects.get(user=user).secret_key

        otp = request.data.get('otp', None)
        if not otp:
            return Response({'error': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)

        totp = pyotp.TOTP(secret_key)
        if totp.verify(otp):
            return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

