from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output

class Acceso(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, line, column):
        Expresion.__init__(self, line, column)
        self.identificador = identificador


    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        #print("Acceso: Que variable debo buscar?", self.identificador)
        valor_variable = ambito.getVariable(self.identificador)
        if valor_variable != None: 
            
         #   print ("ACCESO: tipo y valor de la tabla de simbolos: ",valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
            if valor_variable.tipoSimbolo == Type.STRUCT: 
                #print ("Acceso: WHAT?", valor_variable.atributos)
                return Return(Type.STRUCT, valor_variable) 
            else: 
                #print ("El paso sera por parametro", valor_variable)
                return Return(valor_variable.tipoSimbolo, valor_variable.valorSimbolo) # Al usar Return () indirectamente utilizamos paso por 'parametros' y no por referencia
        else: 
            print ("Error semantico en linea:{}, La variable:'{}' no existe".format( self.line, self.identificador))
            Output.errorSintactico.append(
                Error("La variable:'{}' no existe".format(self.identificador), self.line, self.column)
            ) 
        return  
        