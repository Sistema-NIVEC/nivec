from datetime import date, time

# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────
from clases.enums.modalidad import Modalidad
from clases.enums.tipo_de_identificacion import TipoDeIdentificacion
from clases.enums.perfil_administrativo import PerfilAdministrativo
from clases.enums.tipo_de_vinculacion import TipoDeVinculacion
from clases.enums.tiempo_de_dedicacion import TiempoDeDedicacion
from clases.enums.jornada import Jornada
from clases.enums.registro_de_cupo import RegistroDeCupo
from clases.enums.estado_de_matricula import EstadoDeMatricula
from clases.enums.tipo_de_componente import TipoDeComponente
from clases.enums.dia_de_semana import DiaDeSemana
from clases.enums.tipo_de_sesion import TipoDeSesion
from clases.enums.tipo_de_cohorte import TipoDeCohorte
from clases.enums.tipo_de_informe import TipoDeInforme
from clases.enums.formato_de_exportacion import FormatoDeExportacion
from clases.enums.estado_de_periodo import EstadoDePeriodo
from clases.enums.estado_de_alerta import EstadoDeAlerta
from clases.enums.estado_de_malla import EstadoDeMalla

# ─────────────────────────────────────────────
# Clases del dominio
# ─────────────────────────────────────────────
from clases.universidad import Universidad
from clases.campus import Campus
from clases.carrera import Carrera
from clases.malla_curricular import MallaCurricular
from clases.unidad_curricular import UnidadCurricular
from clases.periodo_de_nivelacion import PeriodoDeNivelacion
from clases.paralelo import Paralelo
from clases.horario import Horario
from clases.cohorte_de_matricula import CohorteDeMatricula
from clases.consolidado_academico import ConsolidadoAcademico
from clases.evaluacion_academica import EvaluacionAcademica
from clases.evaluacion_de_desempeno import EvaluacionDeDesempeno
from clases.incidencia_academica import IncidenciaAcademica
from clases.informe_general import InformeGeneral

# ─────────────────────────────────────────────
# Usuarios
# ─────────────────────────────────────────────
from clases.usuarios.usuario_administrativo import UsuarioAdministrativo
from clases.usuarios.docente import Docente
from clases.usuarios.estudiante import Estudiante
from clases.usuarios.coordinador_dan import CoordinadorDAN
from clases.usuarios.coordinador_unidad_academica import CoordinadorUnidadAcademica

# ─────────────────────────────────────────────
# Servicios
# ─────────────────────────────────────────────
from clases.servicios.distribuidor_de_estudiantes import DistribuidorDeEstudiantes
from clases.servicios.procesador_de_informe import ProcesadorDeInforme
from clases.servicios.monitor_normativo import MonitorNormativo
from clases.servicios.estrategia_de_evaluacion_estandar import EstrategiaDeEvaluacionEstandar
from clases.servicios.depurador_de_sincronizacion import DepuradorDeSincronizacion

# ─────────────────────────────────────────────
# Criterios filtro
# ─────────────────────────────────────────────
from clases.criterios_filtro.criterio_cedula_formato import CriterioCedulaFormato
from clases.criterios_filtro.criterio_consistente_de_horas import CriterioConsistentesDeHoras
from clases.criterios_filtro.criterio_de_periodo_valido import CriterioPeriodoValido


# ══════════════════════════════════════════════════════════════
# UTILIDAD DE IMPRESIÓN
# ══════════════════════════════════════════════════════════════

def seccion(titulo: str):
    print(f"\n{'═' * 60}")
    print(f"  {titulo}")
    print('═' * 60)

def sub(titulo: str):
    print(f"\n── {titulo} ──")

def ok(mensaje: str):
    print(f"  ✔  {mensaje}")

def fallo(mensaje: str):
    print(f"  ✘  {mensaje}")

def resultado(etiqueta: str, valor):
    print(f"  →  {etiqueta}: {valor}")


# ══════════════════════════════════════════════════════════════
# 1. UNIVERSIDAD Y CAMPUS
# ══════════════════════════════════════════════════════════════

seccion("1. UNIVERSIDAD Y CAMPUS")

universidad = Universidad(
    nombre="Universidad Nacional de Nivelación",
    abreviatura="UNN",
    codigo_sniese="SNI-001",
    direccion_matriz="Av. Principal 123, Quito",
    identificador_visual="logo/unn.png"
)
resultado("Info institucional", universidad.recuperar_informacion_institucional())

campus_quito = Campus(
    codigo_de_campus="CAM-001",
    nombre="Campus Quito Norte",
    direccion_fisica="Av. El Inca S/N",
    provincia="Pichincha",
    infraestructura_compartida=False
)
campus_compartido = Campus("CAM-002", "Campus Sur", "Calle 5ta", "Pichincha", True)

resultado("Infraestructura disponible (Quito Norte)", campus_quito.verificar_disponibilidad_de_infraestructura())
resultado("Infraestructura disponible (Sur - compartida)", campus_compartido.verificar_disponibilidad_de_infraestructura())


# ══════════════════════════════════════════════════════════════
# 2. CARRERA
# ══════════════════════════════════════════════════════════════

seccion("2. CARRERA")

carrera_sistemas = Carrera(
    codigo_de_carrera="CAR-TIC-01",
    nombre="Ingeniería en Sistemas",
    modalidad=Modalidad.PRESENCIAL,
    campo_de_conocimiento="Tecnologías de la Información",
    vigencia_sniese=date(2028, 12, 31)
)
carrera_admin = Carrera("CAR-ADM-01", "Administración de Empresas", Modalidad.SEMIPRESENCIAL, "Ciencias Administrativas", date(2027, 6, 30))
carrera_vencida = Carrera("CAR-OLD-01", "Carrera Antigua", Modalidad.VIRTUAL, "Humanidades", date(2020, 1, 1))

resultado("Sistemas activa", carrera_sistemas.esta_activa())
resultado("Carrera vencida activa", carrera_vencida.esta_activa())


# ══════════════════════════════════════════════════════════════
# 3. MALLA CURRICULAR Y UNIDADES CURRICULARES
# ══════════════════════════════════════════════════════════════

seccion("3. MALLA CURRICULAR Y UNIDADES CURRICULARES")

malla_v1 = MallaCurricular(
    codigo_de_malla="MALLA-TIC-001",
    nombre="Malla Nivelación Sistemas v1",
    area_de_conocimiento="TIC",
    duracion_semanas=16,
    version_de_malla="1.0",
    modalidad=Modalidad.PRESENCIAL
)

uc_matematica = UnidadCurricular(
    codigo_de_unidad="UC-MAT-01",
    nombre="Matemáticas Básicas",
    area_de_conocimiento=["Álgebra", "Cálculo"],
    horas_totales=80.0,
    horas_semanales=5.0,
    horas_sincronicas=60.0,
    horas_asincronicas=20.0,
    tipo_de_componente=TipoDeComponente.TEORICO,
    criterio_de_aprobacion=7.0,
    porcentaje_minimo_asistencia=70.0
)

uc_programacion = UnidadCurricular(
    codigo_de_unidad="UC-PROG-01",
    nombre="Fundamentos de Programación",
    area_de_conocimiento=["Algoritmos", "Lógica"],
    horas_totales=100.0,
    horas_semanales=6.0,
    horas_sincronicas=70.0,
    horas_asincronicas=30.0,
    tipo_de_componente=TipoDeComponente.PRACTICO
)

uc_comunicacion = UnidadCurricular(
    codigo_de_unidad="UC-COM-01",
    nombre="Comunicación y Lenguaje",
    area_de_conocimiento=["Redacción", "Comprensión lectora"],
    horas_totales=60.0,
    horas_semanales=4.0,
    horas_sincronicas=40.0,
    horas_asincronicas=20.0,
    tipo_de_componente=TipoDeComponente.TUTORIAL
)

# Agregar unidades individualmente y en lista
ok("Agregando unidades curriculares a la malla")
resultado("Agrega Matemáticas", malla_v1.agregar_unidad_curricular(uc_matematica))
resultado("Agrega Programación", malla_v1.agregar_unidad_curricular(uc_programacion))
resultado("Agrega lista [Comunicación]", malla_v1.agregar_unidad_curricular([uc_comunicacion]))
resultado("Intento duplicado", malla_v1.agregar_unidad_curricular(uc_matematica))
resultado("Total horas nivelación", malla_v1._total_horas_nivelacion)

sub("Validación de horas UC")
resultado("Distribución válida (Matemáticas)", uc_matematica.validar_distribucion_de_horas_totales())
resultado("Info UC Programación", uc_programacion.recuperar_informacion_de_unidad())

sub("Clonar malla (Patrón Prototype)")
malla_v2 = malla_v1.clonar("MALLA-TIC-002", "2.0")
resultado("Código nueva malla", malla_v2.codigo_de_malla)
resultado("Versión clonada", malla_v2.version_de_malla)
resultado("Estado tras clonar", malla_v2._estado.value)
resultado("Unidades heredadas", len(malla_v2._unidades_curriculares))


# ══════════════════════════════════════════════════════════════
# 4. USUARIOS DEL SISTEMA
# ══════════════════════════════════════════════════════════════

seccion("4. USUARIOS DEL SISTEMA")

sub("4a. Usuario Administrativo (Director DAN)")

datos_comunes = dict(
    tipo_de_identificacion=TipoDeIdentificacion.CEDULA,
    sexo="M", etnia="Mestizo",
    porcentaje_de_discapacidad=0.0,
    fecha_de_nacimiento=date(1975, 3, 15)
)

director_dan = UsuarioAdministrativo(
    identificacion="1700000001",
    nombres="Carlos",
    apellidos="Mendoza",
    correo_institucional="c.mendoza@unn.edu.ec",
    contrasena="Admin1234",
    celular="0991234567",
    direccion="Quito Norte",
    identificador_administrativo="ADM-001",
    perfil_administrativo=PerfilAdministrativo.DIRECTOR_DAN,
    **datos_comunes
)
resultado("Login Director DAN", director_dan.iniciar_sesion())

sub("Cambio de contraseña (property setter)")
try:
    director_dan.contrasena = "corta"
except ValueError as e:
    resultado("Contraseña corta rechazada", str(e))

director_dan.contrasena = "NuevaPass99"
ok("Contraseña actualizada correctamente")

sub("4b. Coordinador DAN")

coordinador_dan = CoordinadorDAN(
    identificacion="1700000002",
    nombres="María",
    apellidos="Torres",
    correo_institucional="m.torres@unn.edu.ec",
    contrasena="Coord5678",
    celular="0987654321",
    direccion="Quito Sur",
    identificador_administrativo="ADM-002",
    perfil_administrativo=PerfilAdministrativo.COORDINADOR_DAN,
    identificador_coordinador_dan="CDAN-001",
    **datos_comunes
)
resultado("Login Coordinador DAN", coordinador_dan.iniciar_sesion())

sub("4c. Docentes")

docente_1 = Docente(
    identificacion="1700000010",
    nombres="Ana",
    apellidos="Ruiz",
    correo_institucional="a.ruiz@unn.edu.ec",
    contrasena="Docente01",
    celular="0912345678",
    direccion="Av. América",
    identificador_institucional="DOC-001",
    tipo_de_vinculacion=TipoDeVinculacion.NOMBRAMIENTO,
    tiempo_de_dedicacion=TiempoDeDedicacion.TIEMPO_COMPLETO,
    carga_horaria_maxima=40.0,
    **datos_comunes
)

docente_2 = Docente(
    identificacion="1700000011",
    nombres="Luis",
    apellidos="Vega",
    correo_institucional="l.vega@unn.edu.ec",
    contrasena="Docente02",
    celular="0923456789",
    direccion="Cotocollao",
    identificador_institucional="DOC-002",
    tipo_de_vinculacion=TipoDeVinculacion.CONTRATO,
    tiempo_de_dedicacion=TiempoDeDedicacion.MEDIO_TIEMPO,
    carga_horaria_maxima=20.0,
    **datos_comunes
)

docente_1._especialidades = ["Matemáticas", "Álgebra"]
resultado("Carga académica docente 1", docente_1.visualizar_carga_academica())
resultado("Login docente activo", docente_1.iniciar_sesion())
docente_1.inhabilitar_perfil()
resultado("Login docente inactivo", docente_1.iniciar_sesion())
docente_1._estado_de_vinculacion.__class__  # reactivar para pruebas
from clases.enums.estado_de_vinculacion import EstadoDeVinculacion
docente_1._estado_de_vinculacion = EstadoDeVinculacion.ACTIVO

sub("4d. Coordinador de Unidad Académica (Herencia múltiple)")

coord_ua = CoordinadorUnidadAcademica(
    identificacion="1700000020",
    nombres="Pedro",
    apellidos="Salazar",
    correo_institucional="p.salazar@unn.edu.ec",
    contrasena="CoordUA01",
    celular="0934567890",
    direccion="La Floresta",
    identificador_administrativo="ADM-003",
    perfil_administrativo=PerfilAdministrativo.COORDINADOR_UA,
    identificador_institucional="DOC-003",
    tipo_de_vinculacion=TipoDeVinculacion.NOMBRAMIENTO,
    tiempo_de_dedicacion=TiempoDeDedicacion.TIEMPO_COMPLETO,
    carga_horaria_maxima=40.0,
    identificador_coordinador_ua="CUA-001",
    unidad_academica="Facultad de Ingeniería",
    **datos_comunes
)
resultado("Es instancia UsuarioAdministrativo", isinstance(coord_ua, UsuarioAdministrativo))
resultado("Es instancia Docente", isinstance(coord_ua, Docente))
resultado("Login CoordinadorUA", coord_ua.iniciar_sesion())

sub("4e. Estudiantes")

datos_est = dict(
    tipo_de_identificacion=TipoDeIdentificacion.CEDULA,
    sexo="F", etnia="Mestiza",
    porcentaje_de_discapacidad=0.0,
    fecha_de_nacimiento=date(2004, 7, 20),
    campus_registrado=campus_quito,
    carrera_registrada=carrera_sistemas,
    estado_de_matricula=EstadoDeMatricula.ASPIRANTE
)

def crear_estudiante(id_, nom, ape, correo, mat, jornada, cupo):
    return Estudiante(
        identificacion=id_, nombres=nom, apellidos=ape,
        correo_institucional=correo, contrasena="Estudnt01",
        celular="0900000000", direccion="Quito",
        identificador_institucional=f"EST-{mat[-3:]}",
        numero_de_matricula=mat, jornada=jornada,
        registro_de_cupo=cupo, **datos_est
    )

est_1 = crear_estudiante("1750000001", "Sofía", "López", "s.lopez@unn.edu.ec",
                         "MAT-2024-001", Jornada.MATUTINA, RegistroDeCupo.REGULAR)
est_2 = crear_estudiante("1750000002", "Diego", "Mora",  "d.mora@unn.edu.ec",
                         "MAT-2024-002", Jornada.MATUTINA, RegistroDeCupo.SEGUNDA_MATRICULA)
est_3 = crear_estudiante("1750000003", "Valeria", "Ríos", "v.rios@unn.edu.ec",
                         "MAT-2024-003", Jornada.VESPERTINA, RegistroDeCupo.REGULAR)
est_4 = crear_estudiante("1750000004", "Andrés", "Paz",  "a.paz@unn.edu.ec",
                         "MAT-2024-004", Jornada.MATUTINA, RegistroDeCupo.EXONERACION)

# Flujo de matrícula
resultado("Formalizar matrícula Sofía (ASPIRANTE→MATRICULADO)", est_1.formalizar_matricula())
resultado("Formalizar de nuevo (ya matriculada)", est_1.formalizar_matricula())
resultado("Login Sofía", est_1.iniciar_sesion())

resultado("Formalizar Diego", est_2.formalizar_matricula())
resultado("Formalizar Valeria", est_3.formalizar_matricula())
resultado("Formalizar Andrés", est_4.formalizar_matricula())

resultado("Solicitar retiro Valeria", est_3.solicitar_retiro())
resultado("Login Valeria (retirada)", est_3.iniciar_sesion())


# ══════════════════════════════════════════════════════════════
# 5. HORARIOS Y PARALELOS
# ══════════════════════════════════════════════════════════════

seccion("5. HORARIOS Y PARALELOS")

horario_lunes = Horario(
    dia_semana=DiaDeSemana.LUNES,
    hora_inicio=time(8, 0),
    hora_fin=time(10, 0),
    espacio_de_imparticion="Aula 101",
    modalidad=Modalidad.PRESENCIAL,
    numero_semana=1,
    tipo_de_sesion=TipoDeSesion.SINCRONICA,
    docente_responsable=docente_1
)

horario_martes = Horario(
    dia_semana=DiaDeSemana.MARTES,
    hora_inicio=time(10, 0),
    hora_fin=time(12, 0),
    espacio_de_imparticion="Lab A",
    modalidad=Modalidad.PRESENCIAL,
    numero_semana=1,
    tipo_de_sesion=TipoDeSesion.SINCRONICA,
    docente_responsable=docente_2
)

horario_conflicto = Horario(
    dia_semana=DiaDeSemana.LUNES,
    hora_inicio=time(9, 0),   # solapa con horario_lunes
    hora_fin=time(11, 0),
    espacio_de_imparticion="Aula 102",
    modalidad=Modalidad.PRESENCIAL,
    numero_semana=1,
    tipo_de_sesion=TipoDeSesion.SINCRONICA,
    docente_responsable=docente_1
)

resultado("Duración horario lunes (h)", horario_lunes.determinar_duracion_horas())
resultado("Resumen sesión lunes", horario_lunes.obtener_resumen_de_sesion())
resultado("Conflicto lunes vs martes", horario_lunes.verificar_conflicto_horario(horario_martes))
resultado("Conflicto lunes vs solapado", horario_lunes.verificar_conflicto_horario(horario_conflicto))

sub("Disponibilidad horaria del docente")
docente_1._disponibilidad_semanal.append(horario_lunes)
resultado("Docente 1 disponible para horario conflictivo", docente_1.verificar_disponibilidad_horaria(horario_conflicto))
resultado("Docente 1 disponible para horario martes",     docente_1.verificar_disponibilidad_horaria(horario_martes))

sub("Paralelos")
paralelo_mat = Paralelo("PAR-A", "Paralelo A", Jornada.MATUTINA, Modalidad.PRESENCIAL, capacidad_maxima=3)
paralelo_ves = Paralelo("PAR-B", "Paralelo B", Jornada.VESPERTINA, Modalidad.PRESENCIAL, capacidad_maxima=2)
paralelo_mat.carrera = carrera_sistemas
paralelo_ves.carrera = carrera_sistemas

paralelo_mat.agregar_horario(horario_lunes)
paralelo_mat.agregar_horario(horario_martes)

resultado("Vincular docente al paralelo", paralelo_mat.vincular_docente(docente_1))
resultado("Vincular mismo docente (ya asignado)", paralelo_mat.vincular_docente(docente_1))

resultado("Vincular Sofía",  paralelo_mat.vincular_estudiante(est_1))
resultado("Vincular Diego",  paralelo_mat.vincular_estudiante(est_2))
resultado("Vincular duplicado Sofía", paralelo_mat.vincular_estudiante(est_1))

resultado("Desvincular Diego", paralelo_mat.desvincular_estudiante(est_2))
resultado("Desvincular inexistente", paralelo_mat.desvincular_estudiante(est_4))
resultado("Tiene cupo disponible", paralelo_mat.tiene_cupo_disponible())
resultado("Resumen horario paralelo A", paralelo_mat.obtener_resumen_horario())


# ══════════════════════════════════════════════════════════════
# 6. PERÍODO DE NIVELACIÓN
# ══════════════════════════════════════════════════════════════

seccion("6. PERÍODO DE NIVELACIÓN")

periodo = PeriodoDeNivelacion(
    codigo_periodo="PER-2024-1",
    anio=2024,
    periodo="2024-I",
    fecha_inicio=date(2024, 3, 1),
    fecha_fin=date(2024, 6, 30),
    modalidad=Modalidad.PRESENCIAL,
    numero_periodo=1
)

resultado("Duración en semanas", periodo.calcular_duracion_semanas())
resultado("Resumen planificación", periodo.obtener_resumen_de_planificacion())
resultado("Iniciar (fecha ya pasada → True)", periodo.iniciar_periodo_de_nivelacion())
resultado("Estado tras iniciar", periodo._estado.value)
resultado("Finalizar período", periodo.finalizar_periodo_de_nivelacion())
resultado("Estado final", periodo._estado.value)

sub("Matriz de horarios del período")
resultado("Matriz de horarios", periodo.generar_matriz_de_horarios([paralelo_mat, paralelo_ves]))


# ══════════════════════════════════════════════════════════════
# 7. DISTRIBUIDOR DE ESTUDIANTES
# ══════════════════════════════════════════════════════════════

seccion("7. DISTRIBUIDOR DE ESTUDIANTES")

# Preparar estudiantes y paralelos frescos
paralelo_dist_mat = Paralelo("PAR-DM", "Dist Mat", Jornada.MATUTINA,  Modalidad.PRESENCIAL, 2)
paralelo_dist_ves = Paralelo("PAR-DV", "Dist Ves", Jornada.VESPERTINA, Modalidad.PRESENCIAL, 2)
paralelo_dist_mat.carrera = carrera_sistemas
paralelo_dist_ves.carrera = carrera_sistemas

# est_1=MATUTINA, est_2=MATUTINA, est_4=MATUTINA, est_3=VESPERTINA(retirada pero válida para distribución)
distribuidor = DistribuidorDeEstudiantes([paralelo_dist_mat, paralelo_dist_ves])
no_asignados = distribuidor.distribuir([est_1, est_2, est_4])

resultado("Estudiantes en paralelo matutino", len(paralelo_dist_mat._estudiantes_matriculados))
resultado("No asignados (sin cupo jornada)", no_asignados)


# ══════════════════════════════════════════════════════════════
# 8. COHORTE DE MATRÍCULA
# ══════════════════════════════════════════════════════════════

seccion("8. COHORTE DE MATRÍCULA")

cohorte_sistemas = CohorteDeMatricula(
    codigo_de_registro="COH-2024-01",
    nombre_cohorte="Cohorte Sistemas 2024-I",
    carrera_registrada=carrera_sistemas,
    fecha_de_cierre=date(2030, 12, 31),
    periodo_de_nivelacion=periodo,
    tipo_de_cohorte=TipoDeCohorte.PRIMERA_MATRICULA
)

resultado("Registrar Sofía",  cohorte_sistemas.registrar_estudiante_matriculado(est_1))
resultado("Registrar Diego",  cohorte_sistemas.registrar_estudiante_matriculado(est_2))
resultado("Registrar Andrés", cohorte_sistemas.registrar_estudiante_matriculado(est_4))
resultado("Registrar duplicado", cohorte_sistemas.registrar_estudiante_matriculado(est_1))
resultado("Total matriculados", cohorte_sistemas.calcular_total_matriculados())
resultado("Estadísticas de registro", cohorte_sistemas.obtener_estadisticas_de_registro())


# ══════════════════════════════════════════════════════════════
# 9. CONSOLIDADO ACADÉMICO Y DEPURADOR
# ══════════════════════════════════════════════════════════════

seccion("9. CONSOLIDADO ACADÉMICO Y DEPURADOR DE SINCRONIZACIÓN")

sub("Depurador con criterios filtro")
criterio_cedula   = CriterioCedulaFormato()
criterio_horas    = CriterioConsistentesDeHoras()
criterio_periodo  = CriterioPeriodoValido("2024-I")

depurador = DepuradorDeSincronizacion([criterio_cedula, criterio_horas, criterio_periodo])

matriz_externa = [
    {"cedula": "1750000001", "horas_totales": 80, "horas_sincronicas": 60, "horas_asincronicas": 20, "periodo": "2024-I"},  # válido
    {"cedula": "ABC123",     "horas_totales": 80, "horas_sincronicas": 60, "horas_asincronicas": 20, "periodo": "2024-I"},  # cédula inválida
    {"cedula": "1750000002", "horas_totales": 80, "horas_sincronicas": 50, "horas_asincronicas": 20, "periodo": "2024-I"},  # horas inconsistentes
    {"cedula": "1750000003", "horas_totales": 60, "horas_sincronicas": 40, "horas_asincronicas": 20, "periodo": "2023-II"}, # período distinto
    {"cedula": "1750000004", "horas_totales": 60, "horas_sincronicas": 40, "horas_asincronicas": 20, "periodo": "2024-I"},  # válido
]

depurador.procesar_matriz_externa(matriz_externa)
resultado("Resumen depuración", depurador.obtener_resumen_depuracion())

sub("Consolidado académico")
consolidado = ConsolidadoAcademico(
    periodo_academico=periodo,
    fecha_de_corte=date(2024, 6, 30),
    total_de_cupos_aceptados=5
)
consolidado.cargar_matriz_de_cupos(
    depurador.registros_validos,
    len(depurador.registros_validos),
    len(depurador.registros_con_observaciones)
)
resultado("Verificar cédula válida",    consolidado.verificar_aceptacion_cupo("1750000001"))
resultado("Verificar cédula inválida",  consolidado.verificar_aceptacion_cupo("9999999999"))
resultado("Estadísticas consolidado",   consolidado.obtener_estadisticas_de_consolidado())


# ══════════════════════════════════════════════════════════════
# 10. EVALUACIÓN ACADÉMICA
# ══════════════════════════════════════════════════════════════

seccion("10. EVALUACIÓN ACADÉMICA")

eval_sofia = EvaluacionAcademica(est_1, uc_matematica)
eval_diego = EvaluacionAcademica(est_2, uc_matematica)
eval_andres = EvaluacionAcademica(est_4, uc_matematica)

# Sofía aprueba
eval_sofia.registrar_calificacion(1, 8.5)      # parcial específico
eval_sofia.registrar_calificacion(2, 9.0)
eval_sofia.registrar_asistencia_final(85.0)
eval_sofia.calcular_nota_final()
resultado("Estado aprobación Sofía", eval_sofia.verificar_aprobacion().value)

# Diego reprueba por nota
eval_diego.registrar_calificacion(6.0, 5.5)   # ambos parciales a la vez
eval_diego.registrar_asistencia_final(75.0)
eval_diego.calcular_nota_final()
resultado("Estado aprobación Diego", eval_diego.verificar_aprobacion().value)

# Andrés reprueba por asistencia
eval_andres.registrar_calificacion(1, 9.0)
eval_andres.registrar_calificacion(2, 8.0)
eval_andres.registrar_asistencia_final(55.0)   # < 70%
eval_andres.calcular_nota_final()
resultado("Estado aprobación Andrés (asistencia)", eval_andres.verificar_aprobacion().value)

sub("Resúmenes individuales")
resultado("Resumen Sofía",  eval_sofia.obtener_resumen_de_evaluacion())
resultado("Resumen Diego",  eval_diego.obtener_resumen_de_evaluacion())
resultado("Resumen Andrés", eval_andres.obtener_resumen_de_evaluacion())

sub("Registro de evaluación de paralelo (class method)")
resultado("Evaluación del paralelo", EvaluacionAcademica.registrar_evaluacion_de_paralelo(
    [eval_sofia, eval_diego, eval_andres]
))


# ══════════════════════════════════════════════════════════════
# 11. EVALUACIÓN DE DESEMPEÑO DOCENTE (Strategy)
# ══════════════════════════════════════════════════════════════

seccion("11. EVALUACIÓN DE DESEMPEÑO DOCENTE (Patrón Strategy)")

estrategia_estandar = EstrategiaDeEvaluacionEstandar(
    porcentaje_horas=0.30,
    porcentaje_notas=0.20,
    porcentaje_aprobacion=0.30,
    porcentaje_evaluacion_estudiantil=0.20
)

eval_desempeno = EvaluacionDeDesempeno(
    docente_responsable=docente_1,
    porcentaje_de_horas_cumplidas=95.0,
    entrega_oportuna_de_calificaciones=True,
    porcentaje_de_aprobacion_paralelo=80.0,
    resultado_de_evaluacion_estudiantil=88.0
)

puntaje = eval_desempeno.procesar_evaluacion(estrategia_estandar)
resultado("Puntaje final docente", puntaje)
resultado("Resumen desempeño", eval_desempeno.obtener_resumen_de_desempeno())

sub("Estrategia con entrega tardía de calificaciones")
eval_desempeno_2 = EvaluacionDeDesempeno(docente_2, 80.0, False, 60.0, 75.0)
resultado("Puntaje sin entrega oportuna", eval_desempeno_2.procesar_evaluacion(estrategia_estandar))


# ══════════════════════════════════════════════════════════════
# 12. INCIDENCIA ACADÉMICA
# ══════════════════════════════════════════════════════════════

seccion("12. INCIDENCIA ACADÉMICA")

incidencia = IncidenciaAcademica(
    codigo_incidencia="INC-2024-001",
    docente_implicado=docente_2,
    descripcion="Entrega tardía de calificaciones del parcial 1.",
    fecha_incidencia=date(2024, 4, 20),
    responsable_autorizacion=director_dan
)
resultado("Resumen incidencia", incidencia.obtener_resumen())


# ══════════════════════════════════════════════════════════════
# 13. INFORME GENERAL
# ══════════════════════════════════════════════════════════════

seccion("13. INFORME GENERAL")

informe = InformeGeneral(
    codigo_de_informe="INF-2024-001",
    periodo_academico=periodo,   # ya está CERRADO
    tipo_de_informe=TipoDeInforme.FINAL
)

resultado("Agregar cohorte sistemas", informe.agregar_cohorte_de_matricula(cohorte_sistemas))
resultado("Agregar objeto inválido", informe.agregar_cohorte_de_matricula("no soy cohorte"))

resultado("Total matriculados en informe", informe.obtener_total_matriculados())
resultado("Emitir informe (período CERRADO)", informe.emitir_informe_de_nivelacion())
resultado("Estado del informe", informe._estado_de_informe.value)

evaluaciones = [eval_sofia, eval_diego, eval_andres]
resultado("Consolidado estadísticas", informe.consolidar_estadisticas_institucionales(evaluaciones))
resultado("Tasas de aprobación",       informe.estimar_tasas_de_aprobacion(evaluaciones))
resultado("Retiros y anulaciones",     informe.procesar_retiros_y_anulaciones())

sub("Exportar informe (Procesador)")
procesador = ProcesadorDeInforme()
resultado("Exportar PDF",   procesador.exportar_consolidado(informe, FormatoDeExportacion.PDF))
resultado("Exportar Excel", procesador.exportar_consolidado(informe, FormatoDeExportacion.EXCEL))


# ══════════════════════════════════════════════════════════════
# 14. MONITOR NORMATIVO
# ══════════════════════════════════════════════════════════════

seccion("14. MONITOR NORMATIVO")

monitor = MonitorNormativo()

# Fecha ya vencida
resultado("Alerta período vencido",
    monitor.evaluar_proximidad_vencimiento(periodo, date(2024, 5, 1)))

# Fecha próxima a vencer (5 días desde hoy)
from datetime import timedelta
fecha_prox = date.today() + timedelta(days=3)
resultado("Alerta preventiva (3 días)",
    monitor.evaluar_proximidad_vencimiento(periodo, fecha_prox))

# Fecha normal
fecha_normal = date.today() + timedelta(days=30)
resultado("Alerta normal (30 días)",
    monitor.evaluar_proximidad_vencimiento(periodo, fecha_normal))


# ══════════════════════════════════════════════════════════════
# FIN
# ══════════════════════════════════════════════════════════════

seccion("✔  PRUEBAS COMPLETADAS")
print("  Todas las clases, métodos, patrones y servicios fueron ejercitados.\n")