from Nativas.Return import Return
from Abstractas.Expresion import Expresion

class Acceso(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, line, column):
        Expresion.__init__(self, line, column)
        self.identificador = identificador


    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        valor_variable = ambito.getVariable(self.identificador)
        if valor_variable != None: 
            #print ("ACCESO: tipo y valor de la tabla de simbolos: ",valor_variable.tipoSimbolo, valor_variable.valorSimbolo)

            return Return(valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
        else: 
            print ("Error sintactico: La variable", self.identificador,"no existe")
        return  
        