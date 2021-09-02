from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
import math

class Logaritmo(Expresion):
    def __init__(this, left_exp:Expresion, right_exp:Expresion, line, column):
        Expresion.__init__(this, line, column)
        this.left_expresion  = left_exp
        this.right_expresion = right_exp

    def execute(this, ambito):
        
        base:Return  = this.left_expresion.execute(ambito)
        valor:Return = this.right_expresion.execute(ambito)

        if this.verifyTypes(base.type):

            if this.verifyTypes(valor.type):

                logaritmo_diferente_base = math.log(valor.value, base.value)
                return Return(Type.FLOAT, logaritmo_diferente_base) 
            else: 
                print("Error Sintactico: La funcion log() debe recibir un Int64 o Float64 y recibio:", valor.type)
        else: 
            print("Error Sintactico: La funcion log() debe recibir un Int64 o Float64 y recibio:", base.type)  
        return 

    def verifyTypes(this, actual_type):
        if actual_type == Type.FLOAT or actual_type == Type.INT: 
            return True 
        return False
        