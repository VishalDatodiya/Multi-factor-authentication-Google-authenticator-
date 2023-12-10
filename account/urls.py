from django.urls import path
from account import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp-verification'),
    path('generate-qr-code/', views.generate_qr_code, name='generate-qr-code'),
]
