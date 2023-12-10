# models.py
from django.db import models
from django.contrib.auth.models import User

class OTPSecret(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=16)  # Adjust the length based on your requirements
