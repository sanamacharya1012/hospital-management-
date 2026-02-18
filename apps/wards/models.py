from django.db import models
from django.conf import settings


class Ward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    floor = models.CharField(max_length=50, blank=True)
    nurse_in_charge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nurse_wards",
    )

    def __str__(self):
        return self.name


class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="beds")
    bed_no = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)

    class Meta:
        unique_together = ("ward", "bed_no")

    def __str__(self):
        return f"{self.ward.name} - Bed {self.bed_no}"
