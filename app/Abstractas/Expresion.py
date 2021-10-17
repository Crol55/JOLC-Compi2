from abc import ABC, abstractmethod
# Clase abstracta expresion
''' 
    Expresiones son todas aquellas que retornan valores al operarse
        * Operaciones aritmeticas
        * Operaciones logicas
'''

class Expresion(ABC): 
    
    def __init__(self, line, column):
        self.line = line 
        self.column = column
        # === PROYECTO 2 
        self.trueLabel  = "" 
        self.falseLabel = ""

    @abstractmethod
    def execute(self, ambito): 
        pass

    @abstractmethod 
    def compile(self, ambito): 
        pass