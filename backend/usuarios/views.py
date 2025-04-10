from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages  # Para mostrar mensajes en la plantilla
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from backend.citas.models import Personal  # Importa el modelo Personal

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard")  # Redirigir al nombre de la ruta del dashboard
        else:
            messages.error(request, "❌ Credenciales incorrectas")  # Mensaje de error

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    request.session.flush()  # Eliminar cualquier sesión activa
    return redirect('login')

@login_required
@never_cache
def dashboard_estadistico(request):
    # Obtener el objeto Personal relacionado con el usuario actual
    try:
        personal = Personal.objects.get(usuario=request.user)
        nombre_completo = personal.nombre  # Obtener el nombre del usuario
    except Personal.DoesNotExist:
        nombre_completo = request.user.username  # Si no está en Personal, usa el username

    return render(request, "dashboard.html", {"usuario": nombre_completo})


@login_required
@never_cache
def reportes(request):
    return render(request,"reportes.html")