
from Instrucciones.Transferencia.Continue import Continue
from Instrucciones.Transferencia.Break import Break
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion

class Funcion(Instruccion):
    def __init__(self, id, lista_parametros, lista_instrucciones, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.parametros = lista_parametros
        self.instrucciones = lista_instrucciones
    
    def execute(self, ambito:Ambito):
        # Verificar que las instrucciones ingresadas sean validas para una funcion 
        function_is_valid = True
        for instruccion in self.instrucciones: 
            if type(instruccion) == Funcion: #Una funcion no se puede declarar adentro de otra
                function_is_valid = False
                print("Error Sintactico en linea: {}, No se puede declarar una funcion adentro de otra funcion".format(instruccion.line))
            elif type(instruccion) == Break: 
                function_is_valid = False
                print("Error Sintactico en linea: {}, No se puede declarar un BREAK sin un loop".format(instruccion.line))
            elif type(instruccion) == Continue: 
                function_is_valid = False
                print("Error Sintactico en linea: {}, No se puede declarar un CONTINUE sin un loop".format(instruccion.line))
            
        # Si pasa las validaciones entonces almacenamos la Funcion
        isFunctionSaved = False
        if function_is_valid:
            isFunctionSaved = ambito.saveFunction(self.id, self, self.line) # Almacenamos la clase en el ambito actual
        
        return isFunctionSaved # True:Correct, False:Failed
