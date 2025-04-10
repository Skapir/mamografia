from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

class Paciente(models.Model):
    HI_NREG = models.IntegerField(primary_key=True)
    HI_AUTASE = models.CharField(max_length=255)
    HI_NOMBRE = models.CharField(max_length=255)
    HI_FECNAC = models.DateField()
    HI_UBINAC = models.CharField(max_length=255, default="SIN DATOS")
    HI_DIRECC = models.CharField(max_length=255)
    HI_SEXO = models.CharField(max_length=255)
    HI_NDOCUM = models.CharField(max_length=20, default="SIN DATOS",unique=True)
    HI_ESTCIV = models.CharField(max_length=255)
    HI_CPOLIC = models.CharField(max_length=255, default="valor_por_defecto")

    @property
    def edad_completa(self):
        hoy = date.today()
        nacimiento = self.HI_FECNAC

        diferencia = relativedelta(hoy, nacimiento)
        
        return f"{diferencia.years} A, {diferencia.months} M, {diferencia.days} D"

    def __str__(self):
        return f"{self.HI_NREG} - {self.HI_NOMBRE} - {self.HI_FECNAC}"