from django import forms
from .models import LabOrder, LabResult


class LabOrderForm(forms.ModelForm):
    class Meta:
        model = LabOrder
        fields = ["patient", "doctor", "status"]


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["test", "value", "comment"]
