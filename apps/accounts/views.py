from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User

class HMSLoginView(LoginView):
    template_name = "auth/login.html"

@login_required
def dashboard(request):
    u = request.user
    if u.is_superuser or u.role == User.Role.ADMIN:
        return render(request, "dashboard/admin.html")
    if u.role == User.Role.RECEPTION:
        return render(request, "dashboard/reception.html")
    if u.role == User.Role.NURSE:
        return render(request, "dashboard/nurse.html")
    if u.role == User.Role.DOCTOR:
        return render(request, "dashboard/doctor.html")
    if u.role == User.Role.HR:
        return render(request, "dashboard/hr.html")
