
from Instrucciones.Transferencia.Continue import Continue
from Instrucciones.Transferencia.Break import Break
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output
###################
# Imports PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from compiler.Generator import Generator
from Nativas.Type import Type

class Funcion(Instruccion):
    def __init__(self, id, lista_parametros, tipo_dato, lista_instrucciones, line, column, nodo=None):
        Instruccion.__init__(self, line, column)
        self.id = id 
        self.parametros = lista_parametros
        self.type = tipo_dato
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

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################

    def compile(self, ambito:Ambito):

        temp = Generator() 
        static_gen = temp.getInstance()

        # Verificar que contenga tipo de retorno 
        if (self.type == Type.ANY): # No valido en compilacion pero si en interpretacion..  
            msgError = 'Error en la linea: {}, al "compilar", se debe especificar el tipo de retorno de la funcion'.format(self.line)
            print (msgError)
            static_gen.add_comment(msgError)
            return 

        # Almacenamos la clase como funcion
        ambito.saveFunction(self.id, self, self.line) # Almacenamos esta clase

        # Crear nuevo ambito
        new_ambito = Ambito(ambito)
        new_ambito.size = 1 # size = 0, sera donde se almacenara el return de la funcion. A partir de la posicion 1, iran los parametros de la funcion
        returnLabel = static_gen.generarLabel() 
        new_ambito.returnLabel = returnLabel

        # Guardamos los parametros en el nuevo ambito (Deben tener tipo de dato los parametros )
        # Se pueden manejar sin tipo de dato, pero es mas complejo el codigo 3 direcciones, y el auxiliar dijo que todo vendria tipado
        for parametro  in self.parametros: 
            #print ("Cual es el type?:", parametro.tipo)
            if parametro.tipo != Type.ANY :
                
                storedInHeap = parametro.tipo == (Type.STRING or Type.STRUCT)
                new_ambito.saveVariable_C3D(parametro.id, parametro.tipo, 'local', storedInHeap )
            else:
                errorMsg = "Error en la linea: {}, Los parametros deben tener tipo de dato (::Int64)".format(self.line)
                static_gen.add_comment(errorMsg)
                return None 
        
        static_gen.addBeginOfFuncion(self.id)
        # compilamos las instrucciones que tenga adentro la funcion 
        for instruccion in self.instrucciones: 
            instruccion.compile(new_ambito) 
        
        static_gen.add_goto(returnLabel)
        static_gen.save_label(returnLabel)
        static_gen.addEndOfFuncion() 

        return

        
