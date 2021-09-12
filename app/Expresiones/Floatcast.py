from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion

class Floatcast(Expresion): # convierte un numero entero a uno flotante

    def __init__(self,expresion:Expresion, line, column):
        
        Expresion.__init__(self, line, column)

        self.expresion  = expresion

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito)
        
        if(resultado.type == Type.INT):
            float_cast = float(resultado.value)
            return Return(Type.FLOAT, float_cast)
        else:
            print("Error sintactico: El tipo de dato de la funcion 'float' debe ser un entero y se recibio", resultado.type)
        

    
