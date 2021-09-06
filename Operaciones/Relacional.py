from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from enum import Enum


class OperadorRelacional(Enum):
    GREATER = 0
    LESS    = 1
    GEQ     = 2 
    LEQ     = 3 
    DEQUAL  = 4 
    DISTINT = 5


class Relacional(Expresion):
    def __init__(this, left_expresion:Expresion, right_expresion:Expresion, operador,  line, column):
        Expresion.__init__(this, line, column)
        this.left_expresion = left_expresion
        this.right_expresion = right_expresion
        this.operador = operador
        

    def execute(this, ambito):
        
        resultado_izq:Return = this.left_expresion.execute(ambito)
        resultado_der:Return = this.right_expresion.execute(ambito)

        comparacion = Return(Type.BOOL, False)

        if this.operador == OperadorRelacional.GREATER: 
            comparacion.value = resultado_izq.value > resultado_der.value 
        elif this.operador == OperadorRelacional.LESS: 
            comparacion.value = resultado_izq.value < resultado_der.value
        elif this.operador == OperadorRelacional.GEQ: 
            comparacion.value = resultado_izq.value >= resultado_der.value
        elif this.operador == OperadorRelacional.LEQ: 
            comparacion.value = resultado_izq.value <= resultado_der.value
        elif this.operador == OperadorRelacional.DEQUAL: 
            comparacion.value = resultado_izq.value == resultado_der.value
        elif this.operador == OperadorRelacional.DISTINT: 
            comparacion.value = resultado_izq.value != resultado_der.value
        return comparacion
        