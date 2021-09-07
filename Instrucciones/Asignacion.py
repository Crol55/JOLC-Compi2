
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion

class Asignacion(Instruccion):
    def __init__(self, tipoVariable,verifyType, id, value, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.nombre_variable = id 
        self.expresion = value
        self.alcance = tipoVariable
        self.nodo = nodo
        self.verifyType = verifyType
    
    def execute(self, ambito:Ambito):

        resultado_expresion:Return = self.expresion.execute(ambito)
        #print("ASIGNACION: variable:",self.nombre_variable, resultado_expresion.value, resultado_expresion.type)

        if resultado_expresion.type == self.verifyType or self.verifyType == Type.ANY: 
            #print ("ASIGNACION:      Si puedo almacenar tu variable")
            ambito.saveVariable(self.nombre_variable, resultado_expresion.type, resultado_expresion.value, self.alcance)
            #print ("Imprimiendo el ambito", ambito.variables)
        else: 
            print("Error sintactico: Los tipos de datos de la variable '",self.nombre_variable,"' no coinciden.")
        return  # Si returna None, la ejecucion se realizo correctamente
