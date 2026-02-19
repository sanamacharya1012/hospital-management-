from django import forms
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        field = ["patient", "is_paid"]


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        field = ["description", "qty", "unit_price"]
