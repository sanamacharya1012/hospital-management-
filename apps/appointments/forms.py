from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "scheduled_at", "reason", "status"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }
