
from Tabla_Simbolos.simbolo import simbolo
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

        if resultado_expresion.type == self.verifyType or self.verifyType == Type.ANY: 
            
            if resultado_expresion.type == Type.STRUCT: 
                #if resultado_expresion.value.IdSimbolo == 'Contrato':
                #    self.printearlo(resultado_expresion.value)
                ambito.save_Struct_As_Variable(self.nombre_variable, self.alcance, resultado_expresion.value) 
            else: 
                ambito.saveVariable(self.nombre_variable, resultado_expresion.type, resultado_expresion.value, self.alcance)
            
        elif ( type( self.verifyType) == str and resultado_expresion.type == Type.STRUCT ): # ej, raton = nariz::Nariz
            
            if self.verifyType == resultado_expresion.value.IdSimbolo: # struct.tipo == struct.tipo
                ambito.save_Struct_As_Variable(self.nombre_variable, self.alcance, resultado_expresion.value) 
            else: 
                print ("Asignacion: Error semantico en linea: {}. El tipo de dato compuesto: '{}' no coincide con : '{}'".format(self.line, self.verifyType, resultado_expresion.value.IdSimbolo))
        else: 
            print("Error semantico en linea: {}. Los tipos de datos de la variable '{}' no coinciden.".format(self.line, self.nombre_variable))
            Output.errorSintactico.append(
                Error("Los tipos de datos de la variable:{} no coinciden".format(self.nombre_variable), self.line, self.column)
            ) 
        return  # Si returna None, la ejecucion se realizo correctamente


    def printearlo(self, struct:simbolo):
        print ()
        print ()
        print ("********************** PRINTING STRUCT - ASIGNACION **************************") 
        print (struct.IdSimbolo)
        print (struct.atributos)
        print ("id" ,struct.atributos['actor'].IdSimbolo ,struct.atributos['actor'].atributos)
        print ("********************** FIN PRINTING STRUCT - ASIGNACION **************************") 
        print()
        print()