from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from poo.clases.enums.tipo_de_identificacion import TipoDeIdentificacion
from poo.clases.enums.estado_de_usuario import EstadoDeUsuario
from poo.clases.enums.tipo_de_vinculacion import TipoDeVinculacion
from poo.clases.enums.tiempo_de_dedicacion import TiempoDeDedicacion
from poo.clases.enums.estado_de_vinculacion import EstadoDeVinculacion
from poo.clases.enums.jornada import Jornada
from poo.clases.enums.registro_de_cupo import RegistroDeCupo
from poo.clases.enums.estado_de_matricula import EstadoDeMatricula
from poo.clases.enums.perfil_administrativo import PerfilAdministrativo


def cambiar_enum_a_choices(enum_clase):
    return [(opcion.value, opcion.value) for opcion in enum_clase]


# ══════════════════════════════════════════════════════════════
# GESTOR DE USUARIOS
# ══════════════════════════════════════════════════════════════

class CreadorDeUsuarios(BaseUserManager):

    def create_user(self, correo_institucional, password=None, **kwargs):
        if not correo_institucional:
            raise ValueError("No se ha proporcionado un correo institucional.")
        correo = self.normalize_email(correo_institucional)
        usuario = self.model(correo_institucional=correo, **kwargs)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo_institucional, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(correo_institucional, password, **kwargs)


# ══════════════════════════════════════════════════════════════
# USUARIO DEL SISTEMA (Custom User Model)
# ══════════════════════════════════════════════════════════════

class UsuarioDeSistema(AbstractBaseUser, PermissionsMixin):
    tipo_de_identificacion = models.CharField(
        max_length=50,
        choices=cambiar_enum_a_choices(TipoDeIdentificacion),
        verbose_name="Tipo de identificación"
    )
    identificacion = models.CharField(
        max_length=20, unique=True, verbose_name="Número de identificación"
    )
    nombres = models.CharField(max_length=150, verbose_name="Nombres")
    apellidos = models.CharField(max_length=150, verbose_name="Apellidos")
    correo_institucional = models.EmailField(
        unique=True, verbose_name="Correo institucional"
    )
    fecha_de_nacimiento = models.DateField(
        null=True, blank=True, verbose_name="Fecha de nacimiento"
    )
    sexo = models.CharField(max_length=20, null=True, blank=True, verbose_name="Sexo")
    etnia = models.CharField(max_length=50, null=True, blank=True, verbose_name="Etnia")
    porcentaje_de_discapacidad = models.FloatField(
        default=0.0, null=True, blank=True, verbose_name="Porcentaje de discapacidad"
    )
    celular = models.CharField(
        max_length=15, null=True, blank=True, verbose_name="Número de celular"
    )
    direccion = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="Dirección"
    )
    estado_de_usuario = models.CharField(
        max_length=50,
        choices=cambiar_enum_a_choices(EstadoDeUsuario),
        default=EstadoDeUsuario.PENDIENTE.value,
        verbose_name="Estado de usuario"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CreadorDeUsuarios()

    USERNAME_FIELD = "correo_institucional"
    REQUIRED_FIELDS = ["identificacion", "nombres", "apellidos"]

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.correo_institucional})"
