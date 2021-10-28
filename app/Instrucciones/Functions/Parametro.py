
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion


class Parametro(Instruccion):
    def __init__(self, id, tipo, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.tipo = tipo
        
    
    def execute(self, ambito:Ambito):
        return self # Retorno la clase {id, tipo}

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################
    
    def compile(self, ambito):
        return self # Retorno la clase {id, tipo}
