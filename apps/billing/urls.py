from django.urls import path
from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("add/", views.invoice_add, name="invoice_add"),
    path("<int:invoice_id>/", views.invoice_detail, name="invoice_detail"),
]
