from django.urls import path
from . import views

urlpatterns = [
    path("vitals/add/", views.vitals_add, name="vitals_add"),
    path("notes/add/", views.note_add, name="note_add"),
    path(
        "patient/<int:patient_id>/",
        views.patient_overview,
        name="emr_patient_overview",
    ),
]
