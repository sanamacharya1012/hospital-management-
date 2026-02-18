from django import forms
from .models import Patient, Admission


class PatiensFrom(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["patient_id", "full_name", "dob", "phone", "address", "gender"]


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ["patient", "ward", "bed", "assigned_doctor"]
