from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.patients.models import Admission
from .models import Invoice
from .services import apply_smart_billing


@receiver(post_save, sender=Admission)
def smart_billing_on_discharge(sender, instance: Admission, created, **kwargs):
    if instance.status != Admission.Status.DISCHARGED:
        return
    invoice = Invoice.objects.filter(admission=instance).first()

    if not invoice:
        return
    apply_smart_billing(invoice, instance)
