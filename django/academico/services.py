import openpyxl
import unicodedata
from datetime import date, datetime
from django.db import transaction
from django.http import HttpResponse

from academico.models import (
    Campus, Carrera, PeriodoDeNivelacion, Paralelo, EvaluacionAcademica,
    CohorteDeMatricula, InformeGeneral, ConsolidadoAcademico, MatriculaParalelo,
    Horario, MallaCurricular, UnidadCurricular)
from usuarios.models import PerfilEstudiante
from usuarios.utils import generar_identificador_siguiente

from poo.clases.enums.estado_de_matricula import EstadoDeMatricula
from poo.clases.enums.estado_de_aprobacion import EstadoDeAprobacion
from poo.clases.enums.estado_de_periodo import EstadoDePeriodo
from poo.clases.enums.modalidad import Modalidad
from poo.clases.enums.jornada import Jornada
from poo.clases.enums.tipo_de_cohorte import TipoDeCohorte
from poo.clases.enums.dia_de_semana import DiaDeSemana
from poo.clases.enums.estado_de_malla import EstadoDeMalla

from poo.clases.carrera import Carrera as CarreraBase
from poo.clases.periodo_de_nivelacion import PeriodoDeNivelacion as PeriodoDeNivelacionBase
from poo.clases.evaluacion_academica import EvaluacionAcademica as EvaluacionAcademicaPOO
from poo.clases.horario import Horario as HorarioPOO




# ══════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = str(texto).strip().lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

def obtener_enum_flexible(enum_class, valor_sucio):
    if not valor_sucio:
        return None
    valor_normalizado = normalizar_texto(valor_sucio)
    for opcion in enum_class:
        if normalizar_texto(opcion.value) == valor_normalizado:
            return opcion
    raise ValueError(f"'{valor_sucio}' registro no válido para {enum_class.__name__}")



# ══════════════════════════════════════════════════════════════
# CARGA MASIVA: CAMPUS
# ══════════════════════════════════════════════════════════════

def servicio_campus_registrar_masivo_desde_excel(archivo, universidad_usuario):
    from poo.clases.campus import Campus as CampusBase

    resultado = {"exitosos": 0, "advertencias": [], "error": None}
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active

        nombres_registrados = set()
        for nombre_existente in Campus.objects.filter(universidad=universidad_usuario).values_list("nombre", flat=True):
            nombres_registrados.add(normalizar_texto(nombre_existente))

        for numero_fila, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                nombre = fila[0] if len(fila) > 0 else None
                direccion = fila[1] if len(fila) > 1 else None
                provincia = fila[2] if len(fila) > 2 else None

                if not nombre and not direccion and not provincia:
                    continue

                campus_poo = CampusBase(
                    codigo_de_campus="PENDIENTE",
                    nombre=str(nombre).strip() if nombre else "",
                    direccion_fisica=str(direccion).strip() if direccion else "",
                    provincia=str(provincia).strip() if provincia else "",
                )

                errores_validacion = campus_poo.validar_datos_de_carga_masiva()
                if errores_validacion:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido por falta de información"
                    )
                    continue

                nombre_normalizado = normalizar_texto(campus_poo.nombre)
                if nombre_normalizado in nombres_registrados:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (el Campus ya existe)"
                    )
                    continue

                with transaction.atomic():
                    Campus.objects.create(
                        universidad=universidad_usuario,
                        codigo_de_campus=generar_identificador_siguiente(Campus, 'CAM', 'codigo_de_campus'),
                        nombre=campus_poo.nombre,
                        direccion_fisica=campus_poo.direccion_fisica,
                        provincia=campus_poo.provincia
                    )
                    resultado["exitosos"] += 1
                    nombres_registrados.add(nombre_normalizado)
            except Exception as e:
                resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido ({str(e)})")
                
    except Exception:
        resultado["error"] = "Ha ocurrido un error al procesar el documento"
        
    return resultado




# ══════════════════════════════════════════════════════════════
# CARGA MASIVA: CARRERAS
# ══════════════════════════════════════════════════════════════

def servicio_carrera_registrar_masivo_desde_excel(archivo, universidad_usuario):
    resultado = {"exitosos": 0, "advertencias": [], "error": None}
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active
        
        campus_existente = Campus.objects.filter(universidad=universidad_usuario)

        carreras_registradas = {
            (campus_id, normalizar_texto(nombre_existente))
            for campus_id, nombre_existente in Carrera.objects.filter(
                campus__universidad=universidad_usuario
            ).values_list("campus_id", "nombre")
        }

        for numero_fila, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                codigo_campus = fila[0] if len(fila) > 0 else None
                nombre = fila[1] if len(fila) > 1 else None
                vigencia = fila[2] if len(fila) > 2 else None
                
                if not codigo_campus and not nombre and not vigencia:
                    continue
                
                if not codigo_campus or not nombre or not vigencia:
                    resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido por falta de información")
                    continue

                if isinstance(vigencia, (datetime, date)):
                    vigencia_date = vigencia.date() if isinstance(vigencia, datetime) else vigencia
                elif isinstance(vigencia, str):
                    try:
                        vigencia_date = datetime.strptime(vigencia.strip(), "%Y-%m-%d").date()
                    except ValueError:
                        resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido (formato de fecha no válido)")
                        continue
                else:
                    resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido (formato de fecha no válido)")
                    continue

                campus_obj = campus_existente.filter(codigo_de_campus=str(codigo_campus).strip()).first()
                if not campus_obj:
                    resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido (código de Campus no válido)")
                    continue
                
                carrera_poo = CarreraBase(
                    codigo_de_carrera="PENDIENTE",
                    nombre=str(nombre).strip(),
                    vigencia_sniese=vigencia_date
                )

                if not carrera_poo.esta_activa():
                    resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido (Carrera no vigente)")
                    continue

                clave_carrera = (campus_obj.id, normalizar_texto(nombre))
                if clave_carrera in carreras_registradas:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (la Carrera ya existe)"
                    )
                    continue

                with transaction.atomic():
                    Carrera.objects.create(
                        campus=campus_obj,
                        codigo_de_carrera=generar_identificador_siguiente(Carrera, 'CAR', 'codigo_de_carrera'),
                        nombre=str(nombre).strip(),
                        vigencia_sniese=vigencia_date
                    )
                    resultado["exitosos"] += 1
                    carreras_registradas.add(clave_carrera)
            except Exception as e:
                resultado["advertencias"].append(f"El registro de la fila {numero_fila} fue omitido ({str(e)})")
                
    except Exception:
        resultado["error"] = "Ha ocurrido un error al procesar el documento"
        
    return resultado

# ══════════════════════════════════════════════════════════════
# CARGA MASIVA: MALLAS CURRICULARES
# ══════════════════════════════════════════════════════════════

def servicio_malla_registrar_masivo_desde_excel(archivo, universidad_usuario):
    from poo.clases.malla_curricular import MallaCurricular as MallaCurricularBase
    from poo.clases.enums.estado_de_malla import EstadoDeMalla

    resultado = {"exitosos": 0, "advertencias": [], "error": None}
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active

        carreras_existentes = Carrera.objects.filter(campus__universidad=universidad_usuario)

        mallas_registradas = {
            (carrera_id, str(nombre_existente).strip().lower())
            for carrera_id, nombre_existente in MallaCurricular.objects.filter(
                carrera__campus__universidad=universidad_usuario
            ).values_list("carrera_id", "nombre")
        }

        for numero_fila, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                codigo_carrera, nombre = fila[:2]

                if not any([codigo_carrera, nombre]):
                    continue

                if not all([codigo_carrera, nombre]):
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido por falta de información"
                    )
                    continue

                carrera_obj = carreras_existentes.filter(
                    codigo_de_carrera=str(codigo_carrera).strip()
                ).first()
                if not carrera_obj:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (código de Carrera no válido)"
                    )
                    continue

                malla_poo = MallaCurricularBase(
                    codigo_de_malla="PENDIENTE",
                    nombre=str(nombre).strip(),
                    version_de_malla="PENDIENTE",
                )

                errores_poo = malla_poo.validar_datos_de_registro()
                if errores_poo:
                    primer_error = list(errores_poo.values())[0]
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido ({primer_error})"
                    )
                    continue

                clave_malla = (carrera_obj.id, malla_poo.nombre.strip().lower())
                if clave_malla in mallas_registradas:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (la Malla curricular ya ha sido registrada)"
                    )
                    continue

                with transaction.atomic():
                    MallaCurricular.objects.create(
                        carrera=carrera_obj,
                        codigo_de_malla=generar_identificador_siguiente(
                            MallaCurricular, "MC", "codigo_de_malla"
                        ),
                        nombre=malla_poo.nombre,
                        version_de_malla=servicio_generar_version_malla(carrera_obj),
                        estado=EstadoDeMalla.DISENO.value,
                    )
                    resultado["exitosos"] += 1
                    mallas_registradas.add(clave_malla)

            except Exception as e:
                resultado["advertencias"].append(
                    f"El registro de la fila {numero_fila} fue omitido ({str(e)})"
                )

    except Exception:
        resultado["error"] = "Ha ocurrido un error al procesar el documento"

    return resultado



def servicio_unidad_registrar_masivo_desde_excel(archivo, universidad_usuario):
    from poo.clases.unidad_curricular import UnidadCurricular as UnidadCurricularBase
    from poo.clases.enums.estado_de_malla import EstadoDeMalla
    from academico.models import UnidadCurricular, MallaCurricular
    from usuarios.utils import generar_identificador_siguiente

    estados_editables = (EstadoDeMalla.DISENO.value, EstadoDeMalla.ACTIVA.value)

    resultado = {"exitosos": 0, "advertencias": [], "error": None}
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active

        mallas_existentes = MallaCurricular.objects.filter(
            carrera__campus__universidad=universidad_usuario
        )

        unidades_registradas = {
            (malla_id, str(nombre_u).strip().lower())
            for malla_id, nombre_u in UnidadCurricular.objects.filter(
                malla_curricular__carrera__campus__universidad=universidad_usuario
            ).values_list("malla_curricular_id", "nombre")
        }

        for numero_fila, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            try:
                (codigo_malla, nombre, horas_totales,
                 horas_sincronicas, horas_asincronicas,
                 criterio, porcentaje_asistencia) = fila[:7]

                if not any([codigo_malla, nombre, horas_totales,
                            horas_sincronicas, horas_asincronicas]):
                    continue

                if not all([codigo_malla, nombre, horas_totales,
                            horas_sincronicas, horas_asincronicas]):
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido por falta de información"
                    )
                    continue

                try:
                    horas_totales_f = float(horas_totales)
                    horas_sincronicas_f = float(horas_sincronicas)
                    horas_asincronicas_f = float(horas_asincronicas)
                    criterio_f = float(criterio) if criterio is not None else 7.0
                    porcentaje_f = float(porcentaje_asistencia) if porcentaje_asistencia is not None else 70.0
                except (ValueError, TypeError):
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (registros numéricos no válidos)"
                    )
                    continue

                if horas_sincronicas_f < 6:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (mínimo de horas sincrónicas no válido (6))"
                    )
                    continue

                malla_obj = mallas_existentes.filter(
                    codigo_de_malla=str(codigo_malla).strip()
                ).first()
                if not malla_obj:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (código de Malla no válido)"
                    )
                    continue

                if malla_obj.estado not in estados_editables:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (estado no válido)"
                    )
                    continue

                clave_unidad = (malla_obj.id, str(nombre).strip().lower())
                if clave_unidad in unidades_registradas:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (la Unidad curricular ya ha sido registrada en la Malla especificada)"
                    )
                    continue

                unidad_poo = UnidadCurricularBase(
                    codigo_de_unidad="PENDIENTE",
                    nombre=str(nombre).strip(),
                    horas_totales=horas_totales_f,
                    horas_sincronicas=horas_sincronicas_f,
                    horas_asincronicas=horas_asincronicas_f,
                    criterio_de_aprobacion=criterio_f,
                    porcentaje_minimo_asistencia=porcentaje_f,
                )

                errores_poo = unidad_poo.validar_datos_de_registro()
                if errores_poo:
                    primer_error = list(errores_poo.values())[0]
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido ({primer_error})"
                    )
                    continue

                # Validar límite de horas sincrónicas semanales de la malla (20h)
                from poo.clases.franja_horaria import validar_malla_cabe_en_horario, SEMANAS_REFERENCIA_MINIMA
                from django.db.models import Sum

                suma_existente = UnidadCurricular.objects.filter(
                    malla_curricular=malla_obj
                ).aggregate(total=Sum("horas_sincronicas"))["total"] or 0.0
                total_con_nueva = suma_existente + horas_sincronicas_f
                validacion_malla = validar_malla_cabe_en_horario(total_con_nueva, SEMANAS_REFERENCIA_MINIMA)

                if not validacion_malla["ok"]:
                    resultado["advertencias"].append(
                        f"El registro de la fila {numero_fila} fue omitido (la Malla curricular excede el límite de {validacion_malla['limite']} horas sincrónicas semanales)"
                    )
                    continue

                with transaction.atomic():
                    UnidadCurricular.objects.create(
                        malla_curricular=malla_obj,
                        codigo_de_unidad=generar_identificador_siguiente(
                            UnidadCurricular, "UC", "codigo_de_unidad"
                        ),
                        nombre=unidad_poo.nombre,
                        horas_totales=unidad_poo.horas_totales,
                        horas_sincronicas=unidad_poo.horas_sincronicas,
                        horas_sincronicas_semanales=0,
                        horas_asincronicas=unidad_poo.horas_asincronicas,
                        criterio_de_aprobacion=unidad_poo.criterio_de_aprobacion,
                        porcentaje_minimo_asistencia=unidad_poo.porcentaje_minimo_asistencia,
                    )
                    resultado["exitosos"] += 1
                    unidades_registradas.add(clave_unidad)

            except Exception as e:
                resultado["advertencias"].append(
                    f"El registro de la fila {numero_fila} fue omitido ({str(e)})"
                )

    except Exception:
        resultado["error"] = "Ha ocurrido un error al procesar el documento"

    return resultado