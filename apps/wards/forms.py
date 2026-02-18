from django import forms
from .models import Ward, Bed


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ["name", "floor", "nurse_in_charge"]


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ["ward", "bed_no", "is_occupied"]
