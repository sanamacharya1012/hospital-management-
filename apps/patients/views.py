from decimal import Decimal
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.accounts.decorators import role_required
from apps.accounts.models import User
from apps.billing.models import Invoice, InvoiceItem

from .models import Patient, Admission
from .forms import PatientForm, AdmissionForm


@login_required
def patient_list(request):
    # Admin/Reception : all patients
    if request.user.is_superuser or request.user.role in [
        User.Role.ADMIN,
        User.Role.RECEPTION,
    ]:
        patients = Patient.objects.order_by("-created_at")
        return render(request, "patients/list.html", {"patients": patients})
    # Doctor: only assigned admitted patients

    if request.user.role == User.Role.DOCTOR:
        admissions = (
            Admission.objects.filter(
                status=Admission.Status.ADMITTED, assigned_doctor=request.user
            )
            .select_related("patient")
            .order_by("-admitted_at")
        )
        patients = [a.patient for a in admissions]
        return render(request, "patients/list.html", {"patients": patients})

    # Nurse: only ward admitted patients(where nurse is in-charge)

    if request.user.role == User.Role.NURSE:
        admissions = (
            Admission.objects.filter(
                status=Admission.Status.ADMITTED, ward_nurse_incahrge=request.user
            )
            .select_related("patient")
            .order_by("-admitted_at")
        )
        patients = [a.patient for a in admissions]
        return render(request, "patients/list.html", {"patients": patients})

    # Hr/others
    return render(request, "patients/list.html", {"patients": []})


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION)
def patient_create(request):
    form = PatientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("patient_list")
    return render(request, "patients/form.html", {"form": form, "title": "Add Patient"})


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION)
def admit_patient(request, patient_id=None):
    initial = {}
    if patient_id:
        initial["patient"] = patient_id

    form = AdmissionForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        admission = form.save()
        if admission.bed:
            admission.bed.is_occupied = True
            admission.bed.save()
        return redirect("admission_list")
    return render(
        request, "patients/form.html/", {"form": form, "title": "Admit Patient"}
    )


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION)
def admission_list(request):
    admissions = Admission.objects.select_related(
        "patient", "ward", "bed", "assigned_doctor"
    ).order_by("-admitted_at")
    return render(request, "patients/admissions.html", {"admission": admissions})


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION)
@transaction.atomic
def discharge_patient(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)

    if admission.status == Admission.Status.DISCHARGED:
        return redirect("admission_list")

    admission.status = Admission.Status.DISCHARGED
    admission.discharged_at = timezone.now()
    admission.save()
    if admission.bed:
        admission.bed.is_occupied = False
        admission.bed.save()

    invoice, created = Invoice.objects.get_or_create(
        admission=admission, defaults={"patient": admission.patient, "is_paid": False}
    )

    if created:
        InvoiceItem.objects.create(
            invoice=invoice,
            description="Admission Fee",
            qty=1,
            unit_price=Decimal("500.00"),
        )

        days = 1
        if admission.admitted_at and admission.discharged_at:
            diff = admission.discharged_at.date() - admission.admited_at.date()
            days = max(diff.days, 1)

        InvoiceItem.objects.create(
            invoice=invoice,
            description=f"Bed Charge ({days} day(s))",
            qty=days,
            unit_price=Decimal("1200.00"),
        )

    return redirect("invoice_details", invoice_id=invoice.id)
