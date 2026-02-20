from django.db import models
from django.conf import settings


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "P", "Present"
        ABSENT = "A", "Absent"
        LEAVE = "L", "Leave"
        HALF = "H", "Half Day"

    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PRESENT,
    )

    notes = models.TextField(blank=True)  # ✅ notes (can be long)

    class Meta:
        unique_together = ("staff", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.staff} - {self.date} - {self.get_status_display()}"
