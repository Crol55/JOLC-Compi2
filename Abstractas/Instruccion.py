
from abc import ABC, abstractmethod
# Clase abstracta expresion
''' 
    Instrucciones son todas aquellas que manejarn la tabla de simbolos y ejecutan algo
        * Instruccion para manejor de variables (Asignacion)
'''


class Instruccion(ABC): 
    def __init__(self, line, column):
        self.line = line 
        self.column = column

    @abstractmethod 
    def execute(self, ambito): 
        pass         