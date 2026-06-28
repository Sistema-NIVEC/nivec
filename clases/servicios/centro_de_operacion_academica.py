
from clases.servicios.distribuidor_de_estudiantes import DistribuidorDeEstudiantes
from clases.servicios.procesador_de_informe import ProcesadorDeInforme
#Servicios internos
from clases.servicios.distribuidor_de_estudiantes import DistribuidorDeEstudiantes
from clases.servicios.procesador_de_informe import ProcesadorDeInforme

#Clases
from clases.usuarios.estudiante import Estudiante
from clases.usuarios.usuario_academico import UsuarioAcademico
from clases.usuarios.docente import Docente
from clases.periodo_de_nivelacion import PeriodoDeNivelacion
from clases.evaluacion_academica import EvaluacionAcademica
from clases.informe_general import InformeGeneral
from clases.cohorte_de_matricula import CohorteDeMatricula
from clases.paralelo import Paralelo

#Enums
from clases.enums.formato_de_exportacion import FormatoDeExportacion


class CentroDeOperacionAcademica:
    """
    FACADE

    Punto único de acceso a los principales procesos académicos.

    Coordina los siguientes subsistemas:

    - Estudiantes
    - Docentes
    - Distribución de estudiantes
    - Evaluaciones académicas
    - Periodos de nivelación
    - Cohortes
    - Informes institucionales
    """

    def __init__(self):
        self._distribuidor = DistribuidorDeEstudiantes([])
        self._procesador = ProcesadorDeInforme()

    # ESTUDIANTES

#Simplifica el acceso a los subsistemas complejos de la capa POO.
#Subsistemas:
#-Estudiantes (matrícula, retiro, anulación)
#-Docentes (carga horaria, habilitación)
#-Distribución de estudiantes a paralelos
#-Registro y verificación de evaluaciones académicas
#-Emisión y exportación de informes institucionales
#-Control de periodos de nivelación
#-Administración de cohortes de matrícula


    def _init_(self):
        self._distribuidor = DistribuidorDeEstudiantes([])
        self._procesador = ProcesadorDeInforme()


    #Estudiantes
    def formalizar_matricula(self, estudiante: Estudiante):
        return estudiante.formalizar_matricula()

    def solicitar_retiro(self, estudiante: Estudiante):
        return estudiante.solicitar_retiro()

    def aprobar_retiro(self, estudiante: Estudiante):
        return estudiante.aprobar_retiro()

    def anular_matricula(self, estudiante: Estudiante):
        return estudiante.anular_matricula()

    def obtener_registro_institucional(
        self,
        usuario: UsuarioAcademico
    ):
        return usuario.obtener_registro_institucional()

    # DOCENTES

        estudiante.anular_matricula()


    def obtener_registro_institucional(self, usuario_academico: UsuarioAcademico):
        return usuario_academico.obtener_registro_institucional()


    #Docentes
    def inhabilitar_docente(self, docente: Docente):
        docente.inhabilitar_perfil()

    def obtener_carga_academica(self, docente: Docente):
        return docente.visualizar_carga_academica()

    def verificar_disponibilidad_horaria(
        self,
        docente: Docente,
        horario
    ):
        return docente.verificar_disponibilidad_horaria(horario)


    # DISTRIBUCIÓN DE ESTUDIANTES
    def distribuir_estudiantes(
        self,
        paralelos: list[Paralelo],
        estudiantes: list[Estudiante]
    ):
        self._distribuidor.paralelos = paralelos
        return self._distribuidor.distribuir(estudiantes)

    # EVALUACIONES
    def registrar_evaluacion(
        self,
        evaluacion: EvaluacionAcademica,
        parcial_1: float,
        parcial_2: float,
        porcentaje_asistencia: float
    ):

        evaluacion.registrar_calificacion(
            1,
            parcial_1
        )

        evaluacion.registrar_calificacion(
            2,
            parcial_2
        )

        evaluacion.registrar_asistencia_final(
            porcentaje_asistencia
        )

        nota_final = evaluacion.calcular_nota_final()

        estado = evaluacion.verificar_aprobacion()

        return {
            "nota_final": nota_final,
            "estado": estado
        }

    def obtener_acta_de_paralelo(
        self,
        evaluaciones: list[EvaluacionAcademica]
    ):
        return EvaluacionAcademica.registrar_evaluacion_de_paralelo(
            evaluaciones
        )

    # PERIODO DE NIVELACIÓN

    def iniciar_periodo(
        self,
        periodo: PeriodoDeNivelacion
    ):
        return periodo.iniciar_periodo_de_nivelacion()

    def finalizar_periodo(
        self,
        periodo: PeriodoDeNivelacion
    ):
        return periodo.finalizar_periodo_de_nivelacion()

    def obtener_matriz_de_horarios(
        self,
        periodo: PeriodoDeNivelacion,
        paralelos: list[Paralelo]
    ):
        return periodo.generar_matriz_de_horarios(
            paralelos
        )


    # COHORTES
    def registrar_estudiante_en_cohorte(
        self,
        cohorte: CohorteDeMatricula,
        estudiante: Estudiante
    ):
        return cohorte.registrar_estudiante_matriculado(
            estudiante
        )

    def obtener_estadisticas_de_cohorte(
        self,
        cohorte: CohorteDeMatricula
    ):
        return cohorte.obtener_estadisticas_de_registro()


    # INFORMES
    def emitir_informe(
        self,
        informe: InformeGeneral
    ):
        return informe.emitir_informe_de_nivelacion()

    def exportar_informe(
        self,
        informe: InformeGeneral,
        formato: FormatoDeExportacion
    ):
        return self._procesador.exportar_consolidado(
            informe,
            formato
        )

    def consolidar_estadisticas(
        self,
        informe: InformeGeneral,
        evaluaciones: list
    ):
        return informe.consolidar_estadisticas_institucionales(
            evaluaciones
        )

    def estimar_tasas(
        self,
        informe: InformeGeneral,
        evaluaciones: list
    ):
        return informe.estimar_tasas_de_aprobacion(
            evaluaciones
        )
        
    # OPERACIONES DE ALTO NIVEL (FACADE) 
    def matricular_estudiante(
        self,
        estudiante: Estudiante,
        cohorte: CohorteDeMatricula
    ):
        """
        Formaliza la matrícula y registra al estudiante
        dentro de la cohorte.
        """

        if not estudiante.formalizar_matricula():
            return False

        return cohorte.registrar_estudiante_matriculado(
            estudiante
        )


    def procesar_retiro_de_estudiante(
        self,
        estudiante: Estudiante
    ):
        """
        Gestiona el retiro académico del estudiante.
        """

        return estudiante.solicitar_retiro()


    def registrar_evaluacion_completa(
        self,
        evaluacion: EvaluacionAcademica,
        parcial_1: float,
        parcial_2: float,
        porcentaje_asistencia: float
    ):
        """
        Registra toda la evaluación de un estudiante.
        """

        evaluacion.registrar_calificacion(
            1,
            parcial_1
        )

        evaluacion.registrar_calificacion(
            2,
            parcial_2
        )

        evaluacion.registrar_asistencia_final(
            porcentaje_asistencia
        )

        nota_final = evaluacion.calcular_nota_final()

        estado = evaluacion.verificar_aprobacion()

        return {
            "nota_final": nota_final,
            "estado": estado,
            "resumen": evaluacion.obtener_resumen_de_evaluacion()
        }


    def distribuir_estudiantes_en_paralelos(
        self,
        estudiantes: list[Estudiante],
        paralelos: list[Paralelo]
    ):
        """
        Distribuye automáticamente estudiantes
        entre los paralelos disponibles.
        """

        self._distribuidor.paralelos = paralelos

        no_asignados = self._distribuidor.distribuir(
            estudiantes
        )

        return {
            "total_estudiantes": len(estudiantes),
            "no_asignados": no_asignados
        }


    def iniciar_periodo_academico(
        self,
        periodo: PeriodoDeNivelacion,
        paralelos: list[Paralelo]
    ):
        """
        Inicia el periodo y genera la matriz de horarios.
        """

        if not periodo.iniciar_periodo_de_nivelacion():
            return False

        matriz = periodo.generar_matriz_de_horarios(
            paralelos
        )

        return {
            "periodo_iniciado": True,
            "matriz_de_horarios": matriz
        }


    def cerrar_periodo_academico(
        self,
        periodo: PeriodoDeNivelacion
    ):
        """
        Finaliza el periodo académico.
        """

        return periodo.finalizar_periodo_de_nivelacion()


    def generar_informe_institucional(
        self,
        informe: InformeGeneral,
        evaluaciones: list,
        formato: FormatoDeExportacion
    ):
        """
        Consolida estadísticas, calcula tasas,
        emite el informe y lo exporta.
        """

        estadisticas = (
            informe.consolidar_estadisticas_institucionales(
                evaluaciones
            )
        )

        tasas = (
            informe.estimar_tasas_de_aprobacion(
                evaluaciones
            )
        )

        emitido = informe.emitir_informe_de_nivelacion()

        if not emitido:
            return False

        exportado = self._procesador.exportar_consolidado(
            informe,
            formato
        )

        return {
            "emitido": emitido,
            "exportado": exportado,
            "estadisticas": estadisticas,
            "tasas": tasas
        }


    def cerrar_periodo_y_generar_informe(
        self,
        periodo: PeriodoDeNivelacion,
        informe: InformeGeneral,
        evaluaciones: list,
        formato: FormatoDeExportacion
    ):
        """
        Operación completa de cierre del periodo académico.
        """

        if not periodo.finalizar_periodo_de_nivelacion():
            return False

        return self.generar_informe_institucional(
            informe,
            evaluaciones,
            formato
        )


    def registrar_cohorte_completa(
        self,
        cohorte: CohorteDeMatricula,
        estudiante: Estudiante
    ):
        """
        Registra un estudiante y devuelve
        las estadísticas actualizadas.
        """

        registrado = cohorte.registrar_estudiante_matriculado(
            estudiante
        )

        if not registrado:
            return False

        return {
            "registro": True,
            "estadisticas":
                cohorte.obtener_estadisticas_de_registro()
        }
      
    def verificar_disponibilidad_horaria(self, docente: Docente, horario):
        return docente.verificar_disponibilidad_horaria(horario)


    #Distribución de estudiantes
    def distribuir_estudiantes(self, paralelos: list, estudiantes: list):
        self._distribuidor.paralelos = paralelos
        return self._distribuidor.distribuir(estudiantes)


    #Registro y verificación de evaluaciones
    def registrar_evaluacion(self, evaluacion: EvaluacionAcademica, parcial_1: float, parcial_2: float, porcentaje_asistencia: float):
        evaluacion.registrar_calificacion(1, parcial_1)
        evaluacion.registrar_calificacion(2, parcial_2)
        evaluacion.registrar_asistencia_final(porcentaje_asistencia)
        evaluacion.calcular_nota_final()
        return evaluacion.verificar_aprobacion()

    def obtener_acta_de_paralelo(self, evaluaciones: list):
        return EvaluacionAcademica.registrar_evaluacion_de_paralelo(evaluaciones)


    #Control de periodos de nivelación
    def iniciar_periodo(self, periodo: PeriodoDeNivelacion):
        return periodo.iniciar_periodo_de_nivelacion()

    def finalizar_periodo(self, periodo: PeriodoDeNivelacion):
        return periodo.finalizar_periodo_de_nivelacion()

    def obtener_matriz_de_horarios(self, periodo: PeriodoDeNivelacion, paralelos: list):
        return periodo.generar_matriz_de_horarios(paralelos)


    #Administración de cohortes de matrícula
    def registrar_estudiante_en_cohorte(self, cohorte: CohorteDeMatricula, estudiante: Estudiante):
        return cohorte.registrar_estudiante_matriculado(estudiante)

    def obtener_estadisticas_de_cohorte(self, cohorte: CohorteDeMatricula):
        return cohorte.obtener_estadisticas_de_registro()


    #Emisión y exportación de informes
    def emitir_informe(self, informe: InformeGeneral):
        return informe.emitir_informe_de_nivelacion()

    def exportar_informe(self, informe: InformeGeneral, formato: FormatoDeExportacion):
        return self._procesador.exportar_consolidado(informe, formato)

    def consolidar_estadisticas(self, informe: InformeGeneral, evaluaciones: list):
        return informe.consolidar_estadisticas_institucionales(evaluaciones)

    def estimar_tasas(self, informe: InformeGeneral, evaluaciones: list):
        return informe.estimar_tasas_de_aprobacion(evaluaciones)
