from django.db import models
from django.conf import settings
from apps.patients.models import Patient


class LabTest(models.Model):
    name = models.CharField(max_length=120, unique=True)
    normal_range = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name


class LabOrder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="ORDERED")


class LabResult(models.Model):
    order = models.ForeignKey(
        LabOrder, on_delete=models.CASCADE, related_name="results"
    )
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    value = models.CharField(max_length=120)
    comment = models.CharField(max_length=255, blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
