"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.usuarios.views import login_view,dashboard_estadistico,reportes,logout_view
from backend.citas.views import listado_programacion,guardar_programacion,limpiar_session,aprobar_programacion,busqueda_paciente,registrar_cita,generar_ticket_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name="login"),
    path('', logout_view, name="logout"),
    path('dashboard/',dashboard_estadistico ,name='dashboard_est'),
    path('reportes/',reportes ,name='reportes'),
    path('listado-programacion/',listado_programacion, name="listado_programacion"),
    path("guardar_programacion/", guardar_programacion, name="guardar_programacion"),
    path("limpiar_session/", limpiar_session, name="limpiar_session"),
    path("aprobar-programacion/<int:cupo_id>/", aprobar_programacion, name="aprobar_programacion"),
    path("busqueda-paciente/", busqueda_paciente, name="busqueda_paciente"),
    path("registrar-cita/", registrar_cita, name="registrar_cita"),
    path("ticket/<int:cita_id>/", generar_ticket_pdf, name="generar_ticket_pdf"),
    
]
