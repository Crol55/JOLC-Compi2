

from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
import math

class LogaritmoBaseDiez(Expresion):
    def __init__(this, expresion:Expresion, line, column):
        Expresion.__init__(this, line, column)
        this.expresion = expresion

    def execute(this, ambito):
        
        resultado_expresion:Return = this.expresion.execute(ambito)

        if resultado_expresion.type == Type.FLOAT or resultado_expresion.type == Type.INT:
            logaritmo_base_diez = math.log10(resultado_expresion.value)
            return Return(Type.FLOAT, logaritmo_base_diez)
        else: 
            print("Error Sintactico: La funcion log10() debe recibir un Int64 o Float64 y recibio:", resultado_expresion.type.name)  
        return 
        
