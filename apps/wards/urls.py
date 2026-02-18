from django.urls import path
from . import views

utlpatterns = [
    path("wards/", views.ward_list, name="ward_list"),
    path("wards/add/", views.ward_create, name="ward_add"),
    path("beds/", views.bed_list, name="bed_list"),
    path("bed/add/", views.bed_create, name="bed_add"),
    path("nurse/wards/", views.nurse_wards, name="nurse_wards"),
    path("nurse/patients/", views.nurse_patients, name="nurse_patients"),
]
