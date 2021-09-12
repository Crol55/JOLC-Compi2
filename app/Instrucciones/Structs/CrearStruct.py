

from Instrucciones.Functions.Parametro import Parametro
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion

class CrearStruct(Instruccion):
    
    def __init__(self, isMutable, id, atributos:Parametro, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.isMutable        = isMutable 
        self.id               = id 
        self.lista_parametros = atributos
        

    def execute(self, ambito:Ambito):  # cuando se cree, uniamente hay que guardarlo en la tabla de simbolos (ambito)
        
        isStructSaved = ambito.saveStruct(self.id, self) # Almacena esta misma clase adentro de la tabla de simbolos (ambito)

        return isStructSaved # None: Correct, False: Failed 
