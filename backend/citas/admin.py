from django.contrib import admin
from .models import CentroDeSalud, Personal, Cupo

@admin.register(CentroDeSalud)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("nombre","direccion")

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "centro", "cargo")  # Usar nombres reales del modelo
    list_filter = ("centro",)  # "centro_salud" no existe, debe ser "centro"

@admin.register(Cupo)
class CupoAdmin(admin.ModelAdmin):
    list_display = ("medico", "centro", "fecha", "cantidad")  # Usar "centro" en lugar de "centro_salud"
    list_filter = ("centro", "fecha")  # "centro_salud" no existe, debe ser "centro"
