from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    scheduled_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default="BOOKED")
    created_at = models.DateTimeField(auto_now_add=True)
