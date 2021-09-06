from Nativas.Return import Return
from Abstractas.Expresion import Expresion

class Acceso(Expresion):

    def __init__(self,identificador:str, line, column):
        Expresion.__init__(self, line, column)
        self.identificador = identificador

    def execute(self, ambito):
        print ("Estoy cagado DEL CARLOR ", ambito)
        print ("En que ambito estoy?", ambito.variables)
        valor_variable = ambito.getVariable(self.identificador)
        if valor_variable != None: 
            print ("jiji")
            print (valor_variable.tipoSimbolo)
            print (valor_variable.valorSimbolo)
            return Return(valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
        else: 
            print ("Error sintactico: La variable", self.identificador,"no existe")
        return  
        