from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.citas.models import Cupo

class Command(BaseCommand):
    help = "Actualiza el estado de las programaciones pasadas a 'NO APROBADO'"

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()  # Obtener la fecha actual
        cupos_pasados = Cupo.objects.filter(fecha__lt=hoy, estado="EN PROGRAMACION")

        if cupos_pasados.exists():
            actualizados = cupos_pasados.update(estado="NO APROBADO")  # Obtiene el número de filas afectadas
            self.stdout.write(self.style.SUCCESS(f"✔ {actualizados} programaciones actualizadas a 'NO APROBADO'"))
        else:
            self.stdout.write(self.style.WARNING("⚠ No hay programaciones que actualizar."))
