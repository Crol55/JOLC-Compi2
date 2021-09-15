
from Instrucciones.Transferencia.Continue import Continue
from Instrucciones.Transferencia.Break import Break
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output


class Funcion(Instruccion):
    def __init__(self, id, lista_parametros, lista_instrucciones, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.parametros = lista_parametros
        self.instrucciones = lista_instrucciones
    
    def execute(self, ambito:Ambito):
        # Verificar que las instrucciones ingresadas sean validas para una funcion 
       
        for instruccion in self.instrucciones: 
            if (self.contains_invalid_instructions(instruccion)): 
                return False
            
        # Si pasa las validaciones entonces almacenamos la Funcion
        
        isFunctionSaved = ambito.saveFunction(self.id, self, self.line) # Almacenamos la clase en el ambito actual
        
        return  isFunctionSaved # (None | true): Correct, False:Failed


    def contains_invalid_instructions(self, instruccion):

        if type(instruccion) == Funcion: #Una funcion no se puede declarar adentro de otra
            print("Error Semantico en linea: {}, No se puede declarar una funcion adentro de otra funcion".format(instruccion.line))
            Output.errorSintactico.append(
                Error(" No se puede declarar una funcion adentro de otra funcion", self.line, self.column)
            ) 
            return True

        elif type(instruccion) == Break: 
            print("Error Semantico en linea: {}, No se puede declarar un BREAK sin un loop".format(instruccion.line))
            Output.errorSintactico.append(
                Error(" No se puede declarar un BREAK sin un loop", self.line, self.column)
            )
            return True

        elif type(instruccion) == Continue: 
            print("Error Semantico en linea: {}, No se puede declarar un CONTINUE sin un loop".format(instruccion.line))
            Output.errorSintactico.append(
                Error(" No se puede declarar un CONTINUE sin un loop", self.line, self.column)
            )
            return True
        return False

        
