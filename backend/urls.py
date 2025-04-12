from django.conf import settings
from django.conf.urls.static import static


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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)