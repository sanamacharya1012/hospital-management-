from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.accounts.models import User
from .models import Appointment
from .forms import AppointmentForm


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION)
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("appointment_list")
    return render(
        request, "generic/form.html", {"form": form, "title": "Create Appointment"}
    )


@login_required
@role_required(User.Role.ADMIN, User.Role.RECEPTION, User.Role.DOCTOR)
def appointment_list(request):
    qs = Appointment.objects.select_related("patient", "doctor").order_by(
        "-scheduled_at"
    )
    if request.user.role == User.Role.DOCTOR and not request.user.is_superuser:
        qs = qs.filter(doctor=request.user)
    return render(request, "appointments/list.html", {"appointments": qs})
