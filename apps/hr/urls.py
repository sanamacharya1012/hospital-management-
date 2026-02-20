from django.urls import path
from . import views

urlpatterns = [
    path("mark/", views.attendance_mark, name="attendance_mark"),
    path("report/", views.attendance_report, name="attendance_report"),
]
