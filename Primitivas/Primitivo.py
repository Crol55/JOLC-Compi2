
from Abstractas.Expresion import *
from Nativas.Return import Return
from Nativas.Type import Type 

'''
    Clase para el manejo de valores primitivos 
    * Strings 
    * boolean 
    * char 
    * nothing 
    -------- Los valores primitivos de tipo numerico estan en la clase 'Numerica.py'
'''
class Primitivo(Expresion):
    def __init__(self, rawValue, rawType:Type, line, column):
        Expresion.__init__(self, line, column)

        self.valorPrimitivo = rawValue
        self.tipoDato       = rawType
        #print("val insertado:", rawValue, type(rawValue))

    def execute(self, ambito):
        objetoRetorno = Return(self.tipoDato, self.valorPrimitivo)
        return objetoRetorno
        