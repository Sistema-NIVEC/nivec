clases/servicios/observadores_de_evaluacion.py
from poo.clases.interfaces.i_observador_evaluacion import IObservadorEvaluacion
from poo.clases.enums.estado_de_aprobacion import EstadoDeAprobacion

class ObservadorEstadoEstudiante(IObservadorEvaluacion):
    def actualizar(self, evaluacion_academica):
    #Reacciona al cambio de estado de la evaluación académica del estudiante.
        estudiante = evaluacion_academica.estudiante
        estado_final = evaluacion_academica._estado_de_aprobacion
        
        print(f"(Estudiante): {estudiante.nombres} {estudiante.apellidos}")
        print(f"(Estudiante): {estudiante.identificacion}. Estado de aprobación en {evaluacion_academica.unidad_curricular.nombre}: {estado_final.value}")


class ObservadorInformeGeneral(IObservadorEvaluacion):
    def actualizar(self, evaluacion_academica):
    #Reacciona al cierre de la evaluación académica para enviar los datos de rendimiento hacia el procesamiento de informes.
        if evaluacion_academica._estado_de_aprobacion != EstadoDeAprobacion.PENDIENTE:
            resumen = evaluacion_academica.obtener_resumen_de_evaluacion()
            print(f"(Informe general) Estudiante: {resumen['Estudiante']}. Nota Final: {resumen['Nota final']}")