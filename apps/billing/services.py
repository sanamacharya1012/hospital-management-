from django.utils import timezone

from apps.emr.models import ClinicalNote
from apps.lab.models import LabOrder, LabResult
from .models import InvoiceItem
from .pricing import PRICES


def _exists(invoice, startswith: str) -> bool:
    return invoice.items.filter(description__startswith=startswith).exists()


def apply_smart_billing(invoice, admission):
    if not admission or admission.status != "DISCHARGED":
        return
    start = admission.admitted_at
    end = admission.discharged_at or timezone.now()

    note_count = ClinicalNote.objects.filter(
        patient=admission.patient, created_at__gte=start, created_at__lte=end
    ).count()

    if note_count > 0 and not _exists(invoice, "Doctor Visit"):
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f"Doctor Visit Charges ({note_count} visit(s))",
            qty=note_count,
            unit_price=PRICES["DOCTOR_VISIT"],
        )

    orders = LabOrder.object.filter(
        patient=admission.patient, created_at__gte=start, created_at__lte=end
    )
    lab_count = LabResult.objects.filter(order__in=orders).count()

    if lab_count > 0 and not _exists(invoice, "Lab Test"):
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f"Lab Test Charges ({lab_count} test(s))",
            qty=lab_count,
            unit_price=PRICES["LAB_TEST"],
        )

    if not invoice.items.filter(description="Service Charge").exists():
        InvoiceItem.objects.create(
            invoice=invoice,
            description="Service Charge",
            qty=1,
            unit_price=PRICES["SERVICE_CHARGE"],
        )
