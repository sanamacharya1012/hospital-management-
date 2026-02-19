from django.contrib import admin
from .models import LabTest, LabOrder, LabResult

admin.site.register(LabTest)
admin.site.register(LabOrder)
admin.site.register(LabResult)
