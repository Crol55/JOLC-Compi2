
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion
from Nativas.Type import Type


class Parametro(Instruccion):
    def __init__(self, id, tipo, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.tipo = tipo  
        # Agregado en el 2do proyecto pero tambien puede servir para el primero
        self.tipoCompuesto = "" # Especificamente para structs ( ::Actor)
        
    
    def execute(self, ambito:Ambito): # 1er proyecto
        return self # Retorno la clase {id, tipo}

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################
    
    def compile(self, ambito):

        if ( type(self.tipo) == str ): # Solo ingresa si hay un parametro de tipo struct, (var1 :: Actor)
            
            self.tipoCompuesto = self.tipo 
            self.tipo = Type.STRUCT
        return self # Retorno la clase {id, tipo, tipoCompuesto}
