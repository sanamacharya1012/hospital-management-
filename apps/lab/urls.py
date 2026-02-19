from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.lab_orders, name="lab_orders"),
    path("orders/add/", views.lab_order_add, name="lab_order_add"),
    path("orders?<int:order_id>/", views.lab_order_details, name="lab_order_deyail"),
]
