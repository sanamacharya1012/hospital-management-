from django.contrib import admin
from .models import Vitals, ClinicalNote

admin.site.register(Vitals)
admin.site.register(ClinicalNote)
