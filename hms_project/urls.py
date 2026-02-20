from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("admin/", admin.site.urls),
    path("patients/", include("apps.patients.urls")),
    path("wards/", include("apps.wards.urls")),
    path("appointments/", include("apps.appointments.urls")),
    path("emr/", include("apps.emr.urls")),
    path("lab/", include("apps.lab.urls")),
    path("billing/", include("apps.billing.urls")),
    # path("hr/", include("aaps.hr.urls")),
]
