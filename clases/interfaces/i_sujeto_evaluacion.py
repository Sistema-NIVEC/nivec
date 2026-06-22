clases/interfaces/i_sujeto_evaluacion.py

from abc import ABCMeta
from clases.interfaces.i_observador_evaluacion import IObservadorEvaluacion

class ISujetoEvaluacion(metaclass = ABCMeta):
    def __init__(self):
        self._observadores = [] #Lista de observadores

    def anexar(self, observador: IObservadorEvaluacion):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover(self, observador: IObservadorEvaluacion):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self):
        for obs in self._observadores:
            obs.actualizar(self)  #Se pasa a sí mismo (la instancia del sujeto)