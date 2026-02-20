from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.accounts.decorators import role_required
from apps.accounts.models import User

from .models import Attendance
from .forms import AttendanceForm


@login_required
@role_required(User.Role.ADMIN, User.Role.HR)
def attendance_mark(request):
    form = AttendanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Attendance.objects.update_or_create(
            staff=form.cleaned_data["staff"],
            date=form.cleaned_data["date"],
            defaults={
                "status": form.cleaned_data["status"],
                "notes": form.cleaned_data["notes"],
            },
        )
        return redirect("attendance_report")

    return render(
        request, "generic/form.html", {"form": form, "title": "Mark Attendance"}
    )


@login_required
@role_required(User.Role.ADMIN, User.Role.HR)
def attendance_report(request):
    rows = Attendance.objects.select_related("staff").order_by("-date")[:200]
    return render(request, "hr/report.html", {"rows": rows})
