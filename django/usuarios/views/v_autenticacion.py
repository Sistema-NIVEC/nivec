from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from usuarios import services
from usuarios.models import PerfilAdministrativo, PerfilDocente, PerfilEstudiante
from poo.clases.enums.perfil_administrativo import PerfilAdministrativo as EnumPerfilAdministrativo

@never_cache
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("panel_principal")
    if request.method == "POST":
        correo_institucional = request.POST.get("correo_institucional")
        contrasena = request.POST.get("contrasena")
        resultado_inicio = services.servicio_iniciar_sesion(request, correo_institucional, contrasena)
        if resultado_inicio["exito"]:
            return redirect("panel_principal")
        messages.error(request, resultado_inicio["mensaje"])
    return render(request, "autenticacion/iniciar_sesion.html")


@login_required
def cerrar_sesion(request):
    services.servicio_cerrar_sesion(request)
    return redirect("iniciar_sesion")



