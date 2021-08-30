
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import *
from enum import Enum

class Operador(Enum):
    PLUS  = 0
    MINUS = 1
    MUL   = 2
    DIV   = 3
    POT   = 4
    MOD   = 5


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
        # REALIZAR UNA RESTA
        elif self.operador == Operador.MINUS:
            resultado = self.resta(valorIzquierdo, valorDerecho)
            return resultado
        # Realizar UNA MULTIPLICACION
        elif self.operador == Operador.MUL:
            resultado = self.multiplicacion (valorIzquierdo, valorDerecho)
            return resultado
        # Realizar UNA DIVISION
        elif self.operador == Operador.DIV:
            resultado = self.division (valorIzquierdo, valorDerecho)
            return resultado   
        # Realizar UNA POTENCIA
        elif self.operador == Operador.POT:
            resultado = self.potencia (valorIzquierdo, valorDerecho)
            return resultado 
        # Realizar MODULO
        elif self.operador == Operador.MOD:
            print ("si llego a Modulo")
            resultado = self.modulo (valorIzquierdo, valorDerecho)
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
        elif (operando1.type == Type.FLOAT and operando2.type == Type.FLOAT): # FLOAT, FLOAT
            resultado = operando1.value + operando2.value
            return Return (Type.FLOAT, resultado)
        elif (operando1.type == Type.STRING and operando2.type == Type.STRING): # STRING, STRING
            resultado = operando1.value + operando2.value
            return Return (Type.STRING, resultado)
        else: 
            print("Error: Ocurrio un error Sintactico, no se puede Sumar", operando1.type, "Con", operando2.type)
        return None


    def resta(self, operando1:Return, operando2:Return):
        if (operando1.type == Type.INT and operando2.type == Type.INT):  # ENTERO, ENTERO
            resultado = operando1.value - operando2.value
            return Return(Type.INT, resultado)
        elif (operando1.type ==  Type.INT and operando2.type == Type.FLOAT): 
            resultado = float (operando1.value) - operando2.value 
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.FLOAT and operando2.type == Type.INT):  
            resultado = operando1.value - float (operando2.value )
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.FLOAT and operando2.type == Type.FLOAT):  
            resultado = operando1.value - operando2.value 
            return Return(Type.FLOAT, resultado)
        else: 
            print("Error: Ocurrio un error Sintactico, no se puede restar", operando1.type, "Con", operando2.type)
        return None

    def multiplicacion(self, operando1, operando2):
        if operando1.type == Type.INT and operando2.type == Type.INT:
            resultado = operando1.value * operando2.value
            return Return(Type.INT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.INT:
            resultado = operando1.value * float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.INT and operando2.type == Type.FLOAT:
            resultado = float(operando1.value) * operando2.value 
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.FLOAT:
            resultado = operando1.value * operando2.value 
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.STRING and operando2.type == Type.STRING): # STRING * STRING
            resultado = operando1.value + operando2.value
            return Return (Type.STRING, resultado)
        else: 
            print("Error: Ocurrio un error Sintactico, no se puede mutiplicar", operando1.type, "Con", operando2.type)
        return None

    def division(self, operando1, operando2):
        if operando1.type == Type.INT and operando2.type == Type.INT:
            resultado = float(operando1.value) / float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.INT:
            resultado = operando1.value / float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.INT and operando2.type == Type.FLOAT:
            resultado = float(operando1.value) / operando2.value 
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.FLOAT:
            resultado = operando1.value / operando2.value 
            return Return(Type.FLOAT, resultado)
        return None

    def potencia(self, operando1, operando2):
        if operando1.type == Type.INT and operando2.type == Type.INT: # ENTERO ^ ENTERO
            resultado = operando1.value ** operando2.value
            return Return(Type.INT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.INT: # FLOAT ^ ENTERO
            resultado = operando1.value ** float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.INT and operando2.type == Type.FLOAT:
            resultado = float(operando1.value) ** operando2.value 
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.FLOAT:
            resultado = operando1.value ** operando2.value 
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.STRING and operando2.type == Type.INT): # STRING ^ INT
            resultado = operando1.value * operando2.value
            return Return (Type.STRING, resultado)
        else: 
            print("Error: Ocurrio un error Sintactico, no se puede potenciar", operando1.type, "Con", operando2.type)
        return None

    def modulo(self, operando1, operando2):
        if operando1.type == Type.INT and operando2.type == Type.INT: # ENTERO, ENTERO
            resultado = operando1.value % operando2.value
            return Return(Type.INT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.INT: # FLOAT, ENTERO
            resultado = operando1.value % float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.INT and operando2.type == Type.FLOAT:
            resultado = float(operando1.value) % operando2.value 
            return Return(Type.FLOAT, resultado)
        elif operando1.type == Type.FLOAT and operando2.type == Type.FLOAT:
            resultado = operando1.value % operando2.value 
            return Return(Type.FLOAT, resultado)
        else: 
            print("Error: Ocurrio un error Sintactico, no se puede modular", operando1.type, "Con", operando2.type)
        return None
      
        
    
