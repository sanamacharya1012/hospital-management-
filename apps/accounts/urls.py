from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HMSLoginView, dashboard

urlpatterns = [
    path("login/", HMSLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
]