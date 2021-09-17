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
        print("Que variable debo buscar?", self.identificador)
        valor_variable = ambito.getVariable(self.identificador)
        if valor_variable != None: 
            
            print ("ACCESO: tipo y valor de la tabla de simbolos: ",valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
            if valor_variable.tipoSimbolo == Type.STRUCT: 
                return Return(Type.STRUCT, valor_variable) 
            else: 
                return Return(valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
        else: 
            print ("Error semantico en linea:{}, La variable:'{}' no existe".format( self.line, self.identificador))
            Output.errorSintactico.append(
                Error("La variable:'{}' no existe".format(self.identificador), self.line, self.column)
            ) 
        return  
        