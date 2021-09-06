

from Nativas.Return import Return
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion

class Parametro(Instruccion):
    def __init__(self, id, tipo, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.tipo = tipo
        
    
    def execute(self, ambito:Ambito):
        return self # Retorno la clase {id, tipo}
