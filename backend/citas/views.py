from django.shortcuts import render, redirect
from backend.citas.models import Personal,CentroDeSalud,Cupo,Cita # Importamos el modelo Personal desde usuarios
from backend.usuarios.models import Paciente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils.dateformat import format
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.urls import reverse
import time

def listado_programacion(request):
    usuario = request.user
    hoy = timezone.now().date()  # Obtener la fecha actual

    # Buscar el hospital principal del usuario logueado (CORREGIDO)
    hospital_principal = CentroDeSalud.objects.filter(nombre__icontains=usuario.username, es_principal=True).first()
    
    
    # 🔹 Actualizar estados automáticamente si la fecha ya pasó
    Cupo.objects.filter(fecha__lt=hoy, estado="EN PROGRAMACION").update(estado="NO APROBADO")

    # Buscar cupos después de actualizar los estados
    if hospital_principal:
        medicos = Personal.objects.filter(centro=hospital_principal, cargo="Medico")
        cupos = Cupo.objects.filter(medico__centro=hospital_principal).order_by("fecha")
    else:
        medicos = Personal.objects.none()
        cupos = Cupo.objects.none()

    # ✅ Formatear la fecha antes de enviarla al template
    for cupo in cupos:
        cupo.fecha_formateada = format(cupo.fecha, "d/m/Y")  # Formato día/mes/año  

    # Obtener todos los centros secundarios
    centros_secundarios = CentroDeSalud.objects.filter(es_principal=False)

    # 🔹 FILTROS: Médico, Mes y Centro
    medico_id = request.GET.get("medico")
    mes = request.GET.get("mes")
    centro_id = request.GET.get("centro")
    estado = request.GET.get("estado")
    # Aplicar filtros dinámicamente si existen en la solicitud
    if medico_id:
        cupos = cupos.filter(medico_id=medico_id)

    if mes:
        cupos = cupos.filter(fecha__month=mes)

    if centro_id:
        cupos = cupos.filter(centro_id=centro_id)
    
    if estado:
        cupos = cupos.filter(estado=estado)

    # Diccionario de meses para mostrar en el template
    meses = {
        "1": "Enero", "2": "Febrero", "3": "Marzo", "4": "Abril",
        "5": "Mayo", "6": "Junio", "7": "Julio", "8": "Agosto",
        "9": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }

    

    return render(request, "listado_programacion.html", {
        "medicos": medicos,
        "centros_secundarios": centros_secundarios,
        
        "cupos": cupos,  # Pasamos los cupos filtrados al template
        "today": date.today(),
        "meses": meses,  # Pasamos la lista de meses al template
    })


@login_required
def guardar_programacion(request):
    if request.method == "POST":
        medico_id = request.POST.get("medico")
        centro_id = request.POST.get("centro")
        fecha = request.POST.get("fecha")
        cupos = request.POST.get("cupos")
        turno = request.POST.get("turno")

        # 🔹 Validar que la fecha no sea retroactiva
        if fecha:
            fecha_programada = date.fromisoformat(fecha)
            if fecha_programada < date.today():
                request.session['error_msg'] = "⚠️ No se puede programar en fechas pasadas."
                request.session['open_modal'] = True
                return redirect("listado_programacion")
            
        # Verificar que todos los campos estén completos
        if not all([medico_id, centro_id, fecha, cupos, turno]):
            request.session['error_msg'] = "⚠️ Todos los campos son obligatorios."
            request.session['open_modal'] = True  # 🟢 Activar modal
            return redirect("listado_programacion")

        print("\n📩 Datos recibidos del formulario:")
        print(f"🔹 Medico ID: {medico_id}")
        print(f"🔹 Centro ID: {centro_id}")
        print(f"🔹 Fecha: {fecha}")
        print(f"🔹 Cupos: {cupos}")
        print(f"🔹 Turno: {turno}")

        try:
            # Buscar si ya existe una programación con el mismo médico, fecha y turno
            if Cupo.objects.filter(medico_id=medico_id, fecha=fecha, turno=turno).exists():
                print("❌ Error: Ya existe una programación con este médico, fecha y turno.")
                request.session['error_msg'] = "⚠️ Ya existe una programación para este médico en la misma fecha y turno."
                request.session['open_modal'] = True  # 🟢 Activar modal
                return redirect("listado_programacion")

            # Buscar al médico en la base de datos
            print("\n🔎 Buscando médico en la base de datos...")
            medico = Personal.objects.get(id=medico_id, cargo="Medico")
            print(f"✅ Médico encontrado: {medico.nombre}")

            # Buscar el centro de salud
            print("\n🔎 Buscando centro de salud en la base de datos...")
            centro = CentroDeSalud.objects.get(id=centro_id)
            print(f"✅ Centro encontrado: {centro.nombre}")

            # Validar el usuario que registra la programación
            print("\n🔎 Buscando usuario que registra en la base de datos...")
            try:
                registrado_por = Personal.objects.get(usuario=request.user)
                print(f"✅ Registrado por (Personal): {registrado_por.nombre}")
            except Personal.DoesNotExist:
                registrado_por = request.user  # Si es usuario principal
                print(f"⚠️ Usuario registrado directamente desde auth_user: {registrado_por.username}")

            # Guardar la programación en la base de datos
            print("\n✅ Guardando programación en la base de datos...")
            Cupo.objects.create(
                centro=centro,
                medico=medico,
                fecha=fecha,
                cantidad=cupos,
                cantidad_disponible=cupos,
                turno=turno,
                registrado_por=registrado_por,
                estado="EN PROGRAMACION",
            )

            messages.success(request, "✅ Programación guardada con éxito.")
            
            # 🗑️ Eliminar variables de sesión después de usarlas
            if "open_modal" in request.session:
                del request.session["open_modal"]
            if "error_msg" in request.session:
                del request.session["error_msg"]
            
            return redirect("listado_programacion")

        except Personal.DoesNotExist:
            print("❌ Error: El médico seleccionado no existe.")
            request.session['error_msg'] = "⚠️ El médico seleccionado no existe en la base de datos."
            request.session['open_modal'] = True  # 🟢 Activar modal
        except CentroDeSalud.DoesNotExist:
            print("❌ Error: El centro de salud seleccionado no existe.")
            request.session['error_msg'] = "⚠️ El centro de salud seleccionado no existe en la base de datos."
            request.session['open_modal'] = True  # 🟢 Activar modal
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            request.session['error_msg'] = f"⚠️ Error inesperado: {e}"
            request.session['open_modal'] = True  # 🟢 Activar modal

        return redirect("listado_programacion")

    else:
        messages.error(request, "⚠️ Método no permitido.")
        return redirect("listado_programacion")


@login_required
def limpiar_session(request):
    """ Elimina la variable de sesión 'open_modal' después de ser usada """
    request.session.pop("open_modal", None)
    request.session.pop("error_msg", None)
    return JsonResponse({"status": "success"})


@login_required
@require_POST  # ✅ Solo permite solicitudes POST
def aprobar_programacion(request, cupo_id):

    cupo = get_object_or_404(Cupo, id=cupo_id)
    
    if cupo.estado == "APROBADO":
        return JsonResponse({"error": "Esta programación ya está aprobada."}, status=400)
    
    cupo.estado = "APROBADO"
    cupo.save()
    
    return JsonResponse({"success": "Programación aprobada correctamente."})

@login_required
def busqueda_paciente(request):
    paciente = None
    cupos = []
    centros_principales = CentroDeSalud.objects.filter(es_principal=True)
    centro_usuario = request.user.personal.centro  # El centro del digitador
    hoy = timezone.now().date()

    # Buscar paciente o filtrar programación mediante POST
    if request.method == "POST":
        # Buscar paciente por DNI
        dni = request.POST.get("dni", "").strip()
        if dni:
            if not dni.isdigit() or len(dni) != 8:
                messages.error(request, "El DNI debe contener exactamente 8 dígitos.")
            else:
                try:
                    paciente = get_object_or_404(Paciente, HI_NDOCUM=dni)
                    request.session["dni_paciente"] = dni
                except:
                    messages.error(request, "No se encontró un paciente con este DNI.")
                    return redirect("busqueda_paciente")

        # Filtrar programación
        if "dni_paciente" in request.session:
            paciente = Paciente.objects.get(HI_NDOCUM=request.session["dni_paciente"])

            hospital_id = request.POST.get("centro", "").strip()
            turno = request.POST.get("turno", "").strip()

            filtros = {
                "centro": centro_usuario,               # El centro del digitador
                "estado": "APROBADO",                  # Solo aprobados ✅
                "fecha__gte": hoy                      # Desde hoy en adelante 🗓️
            }

            if hospital_id:
                filtros["medico__centro_id"] = int(hospital_id)
            else:
                filtros["medico__centro__es_principal"] = True

            if turno:
                filtros["turno"] = turno

            cupos = Cupo.objects.filter(**filtros).order_by("fecha")

    return render(request, "busqueda_paciente.html", {
        "paciente": paciente,
        "centros_principales": centros_principales,
        "cupos": cupos,
        "citas" : Cita.objects.filter(dni_paciente=paciente.HI_NDOCUM).order_by("-fecha_registro") if paciente else [],
    })

@login_required
@transaction.atomic
def registrar_cita(request):
    if request.method == "POST":
        dni = request.POST.get("dni")
        cupo_id = request.POST.get("cupo_id")
        numero_solicitud = request.POST.get("numero_solicitud")

        if not all([dni, cupo_id, numero_solicitud]):
            return JsonResponse({"error": "⚠️ Todos los campos son obligatorios."}, status=400)

        try:
            paciente = get_object_or_404(Paciente, HI_NDOCUM=dni)
            cupo = get_object_or_404(Cupo, id=cupo_id)

            if cupo.cantidad_disponible <= 0:
                return JsonResponse({"error": "⚠️ No hay cupos disponibles para esta programación."}, status=400)

            nueva_cita = Cita.objects.create(
                dni_paciente=paciente.HI_NDOCUM,
                cupo=cupo,
                numero_solicitud=numero_solicitud,
                usuario_registro=request.user,
                ip_registro=get_client_ip(request),
            )

            cupo.cantidad_disponible -= 1
            cupo.save()

            pdf_url = reverse("generar_ticket_pdf", args=[nueva_cita.id])
            return JsonResponse({
                "success": True,
                "message": "✅ Cita registrada con éxito.",
                "cita_id": nueva_cita.id,
                "pdf_url": pdf_url
            })

        except Exception as e:
            return JsonResponse({"error": f"❌ Error al registrar la cita: {str(e)}"}, status=500)

    return JsonResponse({"error": "⚠️ Método no permitido."}, status=405)



def get_client_ip(request):
    """Función para capturar IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


@login_required
def generar_ticket_pdf(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    try:
        paciente = Paciente.objects.get(HI_NDOCUM=cita.dni_paciente)
    except Paciente.DoesNotExist:
        paciente = None  # fallback

    context = {
        "cita": cita,
        "paciente": paciente,
    }

    html = render_to_string("ticket_cita.html", context)

    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=ticket-cita-{cita_id}.pdf"
    return response
