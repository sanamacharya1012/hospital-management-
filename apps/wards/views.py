from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.accounts.models import User
from .models import Ward, Bed
from .forms import WardForm, BedForm
from apps.patients.models import Admission


@login_required
@role_required
def ward_list(request):
    wards = Ward.objects.select_related("nurse_in_charge").all()
    return render(request, "wards/ward_list.html", {"wards": wards})


@login_required
@role_required(User.Role.ADMIN)
def ward_create(request):
    form = WardForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("ward_list")
    return render(request, "generic/form.html", {"form": form, "title": "Create Ward"})


@login_required
@role_required(User.Role.ADMIN)
def bed_list(request):
    beds = Bed.objects.select_related("ward").order_by("ward__name", "bed_no")
    return render(request, "wards/bed_list.html", {"beds": beds})


@login_required
@role_required(User.Role.ADMIN)
def bed_create(request):
    form = BedForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("bed_list")
    return render(request, "generic/form.html", {"form": form, "title": "Create Bed"})


@login_required
@role_required(User.Role.NURSE, User.Role.ADMIN)
def nurse_wards(request):
    wards = Ward.objects.filter(nurse_in_charge=request.user).prefetch_related("beds")
    return render(request, "wards/nurse_wards.html", {"wards": wards})


@login_required
@role_required(User.Role.NURSE, User.Role.ADMIN)
def nurse_patients(request):
    admissions = (
        Admission.objects.filter(
            status=Admission.Status.ADMITTED, ward_nurse_in_charge=request.user
        )
        .select_related("paitent", "ward", "bed")
        .order_by("ward_name", "bed__bed_no")
    )
    return render(request, "wards/nurse_patient.html", {"admissions": admissions})
