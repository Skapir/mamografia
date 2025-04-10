from django.db import models
from django.contrib.auth.models import User


class CentroDeSalud(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    es_principal = models.BooleanField(default=False)  # Para identificar hospitales principales
    direccion = models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"

class Personal(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con usuarios Django
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, choices=[
        ('Medico', 'Medico'),
        ('Terminalista', 'Terminalista'),
        ('Programador', 'Programador'),
    ])
    centro = models.ForeignKey(CentroDeSalud, on_delete=models.CASCADE, related_name="personal")

    def __str__(self):
        return f"{self.nombre} - {self.cargo} en {self.centro.nombre}"

class Cupo(models.Model):
    centro = models.ForeignKey(CentroDeSalud, on_delete=models.CASCADE, related_name="cupos")
    medico = models.ForeignKey(Personal, limit_choices_to={'cargo': 'Medico'}, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField(default=0)
    cantidad_disponible = models.PositiveIntegerField(default=0)

    # Nuevos campos
    registrado_por = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="cupos_registrados", null=True)  # Usuario que registra la programación
    turno = models.CharField(max_length=100,null=True)
    estado = models.CharField(max_length=20, default="PROGRAMACION")  # Estado inicial de la programación
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)  # Fecha de creación automática

    def __str__(self):
        return f"{self.medico.nombre} ({self.fecha}) - {self.cantidad} cupos - {self.estado}"


class Cita(models.Model):
    # 🔹 SOLO GUARDAMOS EL DNI del paciente
    dni_paciente = models.CharField(max_length=20)

    # 🔹 Relación con la programación (Cupo)
    cupo = models.ForeignKey("Cupo", on_delete=models.CASCADE)
    numero_solicitud = models.CharField(max_length=20, null=True, blank=True)
    
    # 🔹 Quién registró la cita
    usuario_registro = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_registradas'
    )

    # 🔹 Fecha y hora exacta del registro
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # 🔹 IP desde donde se hizo el registro
    ip_registro = models.GenericIPAddressField(null=True, blank=True)
    atendido = models.BooleanField(default=False)  # Para marcar si la cita fue atendida o no
    def __str__(self):
        return f"Cita para DNI {self.dni_paciente} el {self.cupo.fecha}"