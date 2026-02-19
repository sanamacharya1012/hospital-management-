from django import forms
from .models import Vitals, ClinicalNote


class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = ["patient", "temperature", "bp", "pulse", "spo2"]


class ClinicalNoteForm(forms.ModelForm):
    class Meta:
        model = ClinicalNote
        fields = ["patient", "diagonsis", "treatment_plan", "medications"]
