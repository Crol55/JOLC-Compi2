
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output

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

        #simb = resultado_expresion.value 
        #print ("Variables a asignar", simb.atributos)
        #print("ASIGNACION: variable:",self.nombre_variable, resultado_expresion.value, resultado_expresion.type)

        if resultado_expresion.type == self.verifyType or self.verifyType == Type.ANY: 
            
            if resultado_expresion.type == Type.STRUCT: # var = circulo.color;
                
                ambito.save_Struct_As_Variable(self.nombre_variable, self.alcance, resultado_expresion.value) 
            else: 
                ambito.saveVariable(self.nombre_variable, resultado_expresion.type, resultado_expresion.value, self.alcance)
            #print ("Imprimiendo el ambito", ambito.variables)
        else: 
            print("Error semantico: Los tipos de datos de la variable '",self.nombre_variable,"' no coinciden.")
            Output.errorSintactico.append(
                Error("Los tipos de datos de la variable:{} no coinciden".format(self.nombre_variable), self.line, self.column)
            ) 
        return  # Si returna None, la ejecucion se realizo correctamente
