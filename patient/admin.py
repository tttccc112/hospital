from django.contrib import admin
from .models import Register,Fee,Diagnose,Prescribe,PatientBase,PatientHealth

# Register your models here.
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    pass