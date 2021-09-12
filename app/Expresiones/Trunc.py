from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion

class Trunc(Expresion):

    def __init__(self,type,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)

        self.typeToCast = type 
        self.expresion  = expresion

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito)
        if self.verifyValidCastingTypes(self.typeToCast, resultado.type): 
            valor_truncado = int (resultado.value)
            return Return(Type.INT, valor_truncado)

    def verifyValidCastingTypes(self, typeToCast, actual_type):
        if typeToCast == Type.INT:
            if(actual_type == Type.FLOAT):
                return True 
            else: 
                print ("Error sintactico: El segundo parametro de la funcion trunc debe ser float64")
                return False
        print("Error Sintactico: La conversion unicamente pude realizarse a Int64 y se ingreso", self.typeToCast)
        return False
