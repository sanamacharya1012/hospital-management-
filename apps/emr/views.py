from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.accounts.models import User
from apps.patients.models import Admission
from .models import Vitals, ClinicalNote
from .forms import VitalsForm, ClinicalNoteForm


@login_required
@role_required(User.Role.NURSE, User.Role.ADMIN)
def vitals_add(request):
    form = VitalsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        v = form.save(commit=False)
        v.nurse = request.user
        v.save()
        return redirect("emr_patient_overview", patient_id=v.patient_id)
    return render(request, "generic/form.html", {"form": form, "title": "Add Vitals"})


@login_required
@role_required(User.Role.DOCTOR, User.Role.ADMIN)
def note_add(request):
    form = ClinicalNoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        n = form.save(commit=False)
        n.doctor = request.user
        n.save()
        return redirect("emr_patient_overview", patient_id=n.patient_id)
    return render(
        request, "generic/form.html", {"form": form, "title": "Add Clinical Note"}
    )


@login_required
@role_required(User.Role.ADMIN, User.Role.NURSE, User.Role.DOCTOR, User.Role.RECEPTION)
def patient_overview(request, patient_id):
    vitals = Vitals.objects.filter(patient_id=patient_id).order_by("-created_at")
    notes = ClinicalNote.objects.filter(patient_id=patient_id).order_by("-created_at")
    admission = (
        Admission.objects.filter(patient_id=patient_id).order_by("-admitted_at").first()
    )
    return render(
        request,
        "emr/patient_overview.html",
        {
            "patient_id": patient_id,
            "vitals": vitals,
            "notes": notes,
            "admission": admission,
        },
    )
