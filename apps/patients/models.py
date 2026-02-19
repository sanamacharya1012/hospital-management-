from django.db import models
from django.conf import settings


class Patient(models.Model):
    patient_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"


class Admission(models.Model):
    class Status(models.TextChoices):
        ADMITTED = "ADMITTED", "Admitted"
        DISCHARGED = "DISCHARGED", "Discharged"

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="admission"
    )
    admitted_at = models.DateTimeField(auto_now_add=True)
    discharged_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ADMITTED
    )
    ward = models.ForeignKey(
        "wards.Ward", on_delete=models.SET_NULL, null=True, blank=True
    )
    bed = models.ForeignKey(
        "wards.Bed", on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor_admission",
    )

    def __str__(self):
        return f"{self.patient} - {self.status}"
