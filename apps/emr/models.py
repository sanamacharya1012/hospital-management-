from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class Vitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    bp = models.CharField(max_length=20, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)


class ClinicalNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    diagonsis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    medications = models.TextField(blank=True)
