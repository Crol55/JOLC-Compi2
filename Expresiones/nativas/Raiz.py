from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
import math

class Raiz(Expresion):
    def __init__(this, expresion:Expresion, line, column):
        Expresion.__init__(this, line, column)
        this.expresion = expresion

    def execute(this, ambito):
        
        resultado_expresion:Return = this.expresion.execute(ambito)

        if resultado_expresion.type == Type.FLOAT or resultado_expresion.type == Type.INT:
            raiz_cuadrada = math.sqrt(resultado_expresion.value)
            return Return(Type.FLOAT, raiz_cuadrada)
        else: 
            print("Error Sintactico: La funcion sqrt() debe recibir un Int64 o Float64 y recibio:", resultado_expresion.type.name)  
        return 
        
