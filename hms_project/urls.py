from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False)),
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("patients/", include("apps.patients.urls")),
    path("wards/", include("aaps.wards.urls")),
    path("billing/", include("aaps.billing.urls")),
]
