from decimal import Decimal
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.accounts.decorators import role_required
from apps.accounts.models import User

from .models import Patient, Admission
from .forms import PatiensFrom, AdmissionForm


@login_required
def patient_list(request):
    # Admin/Reception : all patients
    if request.user.is_superuser or request.user.role in [
        User.Role.ADMIN,
        User.Role.RECEPTION,
    ]:
        patients = Patient.objects.order_by("-created_at")
        return render(request, "patient/list.html", {"patients": patients})
