
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion

class Funcion(Instruccion):
    def __init__(self, id, lista_parametros, lista_instrucciones, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.parametros = lista_parametros
        self.instrucciones = lista_instrucciones
    
    def execute(self, ambito:Ambito):
        print ("Se supone que debo ingresar aqui?")
        state = ambito.saveFunction(self.id, self) # Almacenamos la clase en el ambito actual
        return state # True:Correct, False:Failed
