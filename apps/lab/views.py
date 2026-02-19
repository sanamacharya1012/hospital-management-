from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.accounts.models import User
from .models import LabOrder
from .forms import LabOrderForm, LabResultForm


@login_required
@role_required(User.Role.ADMIN, User.Role.DOCTOR)
def lab_order_add(request):
    form = LabOrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lab_orders")
    return render(
        request, "generic/form.html", {"form": form, "title": "Create Lab Orderr"}
    )


@login_required
@role_required(User.Role.ADMIN, User.Role.DOCTOR, User.Role.RECEPTION, User.Role.NURSE)
def lab_orders(request):
    orders = LabOrder.objects.select_related("patients", "doctor").order_by(
        "-created_at"
    )
    if request.user.role == User.Role.DOCTOR and not request.user.is_superuser:
        orders = orders.filter(doctor=request.user)
    return render(request, "lab/orders.html", {"orders": orders})


@login_required
@role_required(User.Role.ADMIN, User.Role.DOCTOR)
def lab_order_details(request, order_id):
    order = get_object_or_404(LabOrder, id=order_id)
    form = LabResultForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        r = form.save(commit=False)
        r.order = order.save()
        order.status = "REPORTED"
        order.save()
        return redirect("lab_order_detail", order_id=order.id)
    return render(request, "lab/order_detail.html", {"order": order, "form": form})
