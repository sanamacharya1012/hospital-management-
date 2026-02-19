from django.db import models
from apps.patients.models import Patient


class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.OneToOneField(
        "patients.Admission", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=True)

    def total(self):
        return sum(i.line_total() for i in self.items.all())


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="item")
    description = models.CharField(max_length=255)
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.qty * self.unit_price
