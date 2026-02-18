from django.urls import path
from . import views

urlpatterns = [
    path("", views.patient_list, name="patient_list"),
    path("add/", views.patient_create, name="patient_add"),
    path("admissions/", views.admission_list, name="admission_list"),
    path("admit/", views.admit_patient, name="admit_patient"),
    path(
        "admit/<int:patient_id>/", views.admit_patient, name="admit-patient_for_patient"
    ),
    path(
        "discharge/<int:admission_id>/",
        views.discharge_patient,
        name="discharge_patient",
    ),
]
