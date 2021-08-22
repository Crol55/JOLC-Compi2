
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import *
from enum import Enum

class Operador(Enum):
    PLUS  = 0
    MINUS = 1
    MUL   = 2
    DIV   = 3


class Aritmeticas(Expresion): 
    def __init__(self, leftExpression:Expresion,operador, rightExpression:Expresion, line, column):

        super().__init__(line, column)
        self.leftExpression  = leftExpression 
        self.rightExpression = rightExpression
        self.operador = operador

    def execute(self, ambito):
        valorIzquierdo:Return = self.leftExpression.execute(None)
        valorDerecho:Return   = self.rightExpression.execute(None)

        # REALIZAR UNA SUMA
        if self.operador == Operador.PLUS: 
            resultado = self.suma(valorIzquierdo, valorDerecho)
            return resultado


    def suma(self, operando1, operando2): 
        # Validar que la suma, tenga tipos aceptables
        if (operando1.type == Type.INT and operando2.type == Type.INT):      # ENTERO, ENTERO
            resultado = operando1.value + operando2.value
            return Return(Type.INT, resultado)
        elif (operando1.type == Type.FLOAT and operando2.type == Type.INT):  # FLOAT, ENTERO
            resultado = float(operando1.value) + float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.INT and operando2.type == Type.FLOAT):  # ENTERO, FLOAT
            print("ejecuto el correcto")
            resultado = float(operando1.value) + float(operando2.value)
            return Return(Type.FLOAT, resultado)

        print("Error ese tipo de dato no se puede sumar")
        return None

        
    
