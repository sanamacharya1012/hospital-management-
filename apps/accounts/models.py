from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECEPTION = "RECEPTION", "Reception"
        NURSE = "NURSE", "Nurse"
        DOCTOR = "DOCTOR", "Doctor"
        HR = "HR", "HR"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECEPTION)
