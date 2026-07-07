from django.db import models

from poo.clases.enums.modalidad import Modalidad
from poo.clases.enums.estado_de_malla import EstadoDeMalla
from poo.clases.enums.estado_de_periodo import EstadoDePeriodo
from poo.clases.enums.jornada import Jornada
from poo.clases.enums.dia_de_semana import DiaDeSemana
from poo.clases.enums.tipo_de_cohorte import TipoDeCohorte
from poo.clases.enums.estado_de_cohorte import EstadoDeCohorte
from poo.clases.enums.estado_de_aprobacion import EstadoDeAprobacion
from poo.clases.enums.tipo_de_informe import TipoDeInforme
from poo.clases.enums.estado_de_informe import EstadoDeInforme


def cambiar_enum_a_choices(enum_clase):
    """Convierte un Enum en una lista de tuplas (valor, valor) para Django choices."""
    return [(opcion.value, opcion.value) for opcion in enum_clase]


# ══════════════════════════════════════════════════════════════
# ESTRUCTURA INSTITUCIONAL
# ══════════════════════════════════════════════════════════════

class Universidad(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la institución")
    abreviatura = models.CharField(max_length=20, verbose_name="Abreviatura")
    codigo_sniese = models.CharField(max_length=50, unique=True, verbose_name="Código SNIESE")
    direccion_matriz = models.CharField(
        max_length=300, blank=True, default="", verbose_name="Dirección de matriz"
    )
    identificador_visual = models.ImageField(
        upload_to="logos/", null=True, blank=True, verbose_name="Identificador visual"
    )

    class Meta:
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"


class Campus(models.Model):
    universidad = models.ForeignKey(
        Universidad, on_delete=models.PROTECT,
        related_name="campus", verbose_name="Universidad registrada"
    )
    codigo_de_campus = models.CharField(max_length=50, unique=True, verbose_name="Código de campus")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    direccion_fisica = models.CharField(max_length=300, verbose_name="Dirección física")
    provincia = models.CharField(max_length=100, blank=True, default="", verbose_name="Provincia")

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campus"

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    campus = models.ForeignKey(
        Campus, on_delete=models.PROTECT,
        related_name="carreras", verbose_name="Campus registrado"
    )
    codigo_de_carrera = models.CharField(max_length=50, unique=True, verbose_name="Código de carrera")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    vigencia_sniese = models.DateField(verbose_name="Vigencia SNIESE")

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    def __str__(self):
        return self.nombre


# ══════════════════════════════════════════════════════════════
# ESTRUCTURA CURRICULAR
# ══════════════════════════════════════════════════════════════

class MallaCurricular(models.Model):
    carrera = models.ForeignKey(
        Carrera, on_delete=models.PROTECT,
        related_name="mallas_curriculares", verbose_name="Carrera registrada"
    )
    codigo_de_malla = models.CharField(max_length=50, unique=True, verbose_name="Código de Malla curricular")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    version_de_malla = models.CharField(max_length=20, verbose_name="Versión de Malla curricular")
    estado = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(EstadoDeMalla),
        default=EstadoDeMalla.DISENO.value, verbose_name="Estado"
    )
    total_horas_nivelacion = models.FloatField(default=0.0, verbose_name="Total de horas de nivelación")

    class Meta:
        verbose_name = "Malla curricular"
        verbose_name_plural = "Mallas curriculares"

    def __str__(self):
        return f"{self.codigo_de_malla} ({self.nombre})"


class UnidadCurricular(models.Model):
    malla_curricular = models.ForeignKey(
        MallaCurricular, on_delete=models.PROTECT,
        related_name="unidades_curriculares", verbose_name="Malla curricular registrada"
    )
    codigo_de_unidad = models.CharField(max_length=50, unique=True, verbose_name="Código de unidad curricular")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    horas_totales = models.FloatField(verbose_name="Horas totales")
    horas_sincronicas = models.FloatField(verbose_name="Horas sincrónicas")
    horas_sincronicas_semanales = models.FloatField(default=0, verbose_name="Horas sincrónicas semanales")
    horas_asincronicas = models.FloatField(verbose_name="Horas asincrónicas")
    criterio_de_aprobacion = models.FloatField(default=7.0, verbose_name="Criterio de aprobación")
    porcentaje_minimo_asistencia = models.FloatField(default=70.0, verbose_name="Porcentaje mínimo de asistencia")

    class Meta:
        verbose_name = "Unidad curricular"
        verbose_name_plural = "Unidades curriculares"

    def __str__(self):
        return f"{self.codigo_de_unidad} ({self.nombre})"

# ══════════════════════════════════════════════════════════════
# PERIODO DE NIVELACIÓN
# ══════════════════════════════════════════════════════════════

class PeriodoDeNivelacion(models.Model):
    universidad = models.ForeignKey(
        Universidad, on_delete=models.PROTECT,
        related_name="periodos_de_nivelacion", verbose_name="Universidad registrada"
    )
    codigo_periodo = models.CharField(max_length=50, unique=True, verbose_name="Código de periodo de nivelación")
    anio = models.IntegerField(verbose_name="Año")
    periodo = models.CharField(max_length=50, verbose_name="Periodo")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de finalización")
    numero_de_semanas = models.IntegerField(default=8, verbose_name="Número de semanas")
    modalidad = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(Modalidad), verbose_name="Modalidad"
    )
    numero_periodo = models.IntegerField(verbose_name="Número de periodo de nivelación")
    estado = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(EstadoDePeriodo),
        default=EstadoDePeriodo.PLANIFICACION.value, verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Periodo de nivelación"
        verbose_name_plural = "Periodos de nivelación"

    def __str__(self):
        return f"{self.periodo} ({self.estado})"


# ══════════════════════════════════════════════════════════════
# PARALELOS Y HORARIOS
# ══════════════════════════════════════════════════════════════

class Paralelo(models.Model):
    periodo_de_nivelacion = models.ForeignKey(
        PeriodoDeNivelacion, on_delete=models.PROTECT,
        related_name="paralelos", verbose_name="Periodo de nivelación registrado"
    )
    unidad_curricular = models.ForeignKey(
        UnidadCurricular, on_delete=models.PROTECT,
        related_name="paralelos", verbose_name="Unidad curricular"
    )
    codigo_de_paralelo = models.CharField(max_length=50, verbose_name="Código de paralelo")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    jornada = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(Jornada), verbose_name="Jornada"
    )
    modalidad = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(Modalidad), verbose_name="Modalidad"
    )
    capacidad_maxima = models.IntegerField(default=35, verbose_name="Número máximo de estudiantes")
    docente_responsable = models.ForeignKey(
        'usuarios.PerfilDocente', on_delete=models.SET_NULL,
        null=True, blank=True, related_name="paralelos", verbose_name="Docente responsable"
    )

    class Meta:
        verbose_name = "Paralelo"
        verbose_name_plural = "Paralelos"

    def __str__(self):
        return f"{self.nombre} ({self.unidad_curricular.nombre})"

    def tiene_cupo_disponible(self):
        total_matriculados = self.estudiantes_matriculados.count()
        return total_matriculados < self.capacidad_maxima


class Horario(models.Model):
    paralelo = models.ForeignKey(
        Paralelo, on_delete=models.CASCADE,
        related_name="horarios", verbose_name="Paralelo registrado"
    )
    dia_semana = models.CharField(
        max_length=20, choices=cambiar_enum_a_choices(DiaDeSemana), verbose_name="Día de semana"
    )
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de finalización")
    espacio_de_imparticion = models.CharField(
        max_length=200, blank=True, default="", verbose_name="Espacio de impartición"
    )

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.dia_semana}: {self.hora_inicio}-{self.hora_fin} ({self.paralelo.nombre})"

    def determinar_duracion_horas(self):
        from poo.clases.horario import Horario as HorarioBase
        from poo.clases.enums.dia_de_semana import DiaDeSemana as DiaBase

        horario = HorarioBase(
            dia_semana=DiaBase(self.dia_semana),
            hora_inicio=self.hora_inicio,
            hora_fin=self.hora_fin,
            espacio_de_imparticion=self.espacio_de_imparticion,
        )
        return horario.determinar_duracion_horas()


# ══════════════════════════════════════════════════════════════
# MATRÍCULAS Y COHORTES
# ══════════════════════════════════════════════════════════════

class CohorteDeMatricula(models.Model):
    periodo_de_nivelacion = models.ForeignKey(
        PeriodoDeNivelacion, on_delete=models.PROTECT,
        related_name="cohortes_de_matricula", verbose_name="Periodo de nivelación registrado"
    )
    carrera_registrada = models.ForeignKey(
        Carrera, on_delete=models.PROTECT,
        related_name="cohortes", verbose_name="Carrera registrada"
    )
    codigo_de_registro = models.CharField(max_length=50, unique=True, verbose_name="Código de registro")
    nombre_cohorte = models.CharField(max_length=200, verbose_name="Nombre")
    fecha_de_cierre = models.DateField(verbose_name="Fecha de cierre")
    tipo_de_cohorte = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(TipoDeCohorte),
        verbose_name="Tipo de cohorte de matrícula"
    )
    estado_de_cohorte = models.CharField(
        max_length=50, choices=cambiar_enum_a_choices(EstadoDeCohorte),
        default=EstadoDeCohorte.ABIERTA.value, verbose_name="Estado"
    )
    total_primera_matricula = models.IntegerField(default=0, verbose_name="Número de primeras matrículas")
    total_segunda_matricula = models.IntegerField(default=0, verbose_name="Número de segundas matrículas")
    total_exonerados = models.IntegerField(default=0, verbose_name="Número de exonerados")

    class Meta:
        verbose_name = "Cohorte de matrícula"
        verbose_name_plural = "Cohortes de matrícula"

    def __str__(self):
        return f"{self.codigo_de_registro} ({self.tipo_de_cohorte})"

    def calcular_total_matriculados(self):
        from poo.clases.cohorte_de_matricula import CohorteDeMatricula as CohorteDeMatriculaBase
        from poo.clases.enums.tipo_de_cohorte import TipoDeCohorte as TipoCohorteBase

        cohorte_de_matricula = CohorteDeMatriculaBase(
            codigo_de_registro=self.codigo_de_registro,
            periodo_de_nivelacion=None,
            carrera_registrada=None,
            fecha_de_cierre=self.fecha_de_cierre,
            tipo_de_cohorte=TipoCohorteBase(self.tipo_de_cohorte)
        )
        cohorte_de_matricula.total_primera_matricula = self.total_primera_matricula
        cohorte_de_matricula.total_segunda_matricula = self.total_segunda_matricula
        cohorte_de_matricula.total_exonerados = self.total_exonerados

        return cohorte_de_matricula.calcular_total_matriculados()



    