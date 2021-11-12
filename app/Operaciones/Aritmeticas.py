

from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import *
from enum import Enum
from Nativas.Error import Error
from Export import Output
# proyecto2 
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler

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
        valorIzquierdo:Return = self.leftExpression.execute(ambito)
        valorDerecho:Return   = self.rightExpression.execute(ambito)

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
            
            resultado = float(operando1.value) + float(operando2.value)
            return Return(Type.FLOAT, resultado)
        elif (operando1.type == Type.FLOAT and operando2.type == Type.FLOAT): # FLOAT, FLOAT
            resultado = operando1.value + operando2.value
            return Return (Type.FLOAT, resultado)
        elif (operando1.type == Type.STRING and operando2.type == Type.STRING): # STRING, STRING
            resultado = operando1.value + operando2.value
            return Return (Type.STRING, resultado)
        else: 
            print("Error semantico en linea: {}, no se puede Sumar: {} con {}.".format(self.line, operando1.type, operando2.type) )
            aritmeticError = Error('No se puede sumar {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
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
            aritmeticError = Error('No se puede restar {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
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
            print("Error Sintactico en linea {}:, no se puede multiplicar {} con {}.".format(self.line, operando1.type, operando2.type) )
            aritmeticError = Error('No se puede multiplicar {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
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
        else: 
            print("Error Sintactico en linea {}:, no se puede dividir {} con {}.".format(self.line, operando1.type, operando2.type) )
            aritmeticError = Error('No se puede dividir {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
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
            print("Error Sintactico en linea {}:, no se puede potenciar {} con {}.".format(self.line, operando1.type, operando2.type) )
            aritmeticError = Error('No se puede potenciar {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
        return 

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
            print("Error Sintactico en linea {}:, no se puede modular {} con {}.".format(self.line, operando1.type, operando2.type) )
            aritmeticError = Error('No se puede aplicar modulo a {} con {}'.format(operando1.type, operando2.type), self.line, self.column)
            Output.errorSintactico.append(aritmeticError)
        return None
      

    ########## 
    # El codigo de abajo es para el proyecto 2 - C3D (codigo 3 direcciones)
    ##########
    def compile(self, ambito):

        aux_generator = Generator() 
        static_generator = aux_generator.getInstance() 
        
        valorIzquierdo = self.leftExpression.compile(ambito)
        valorDerecho = self.rightExpression.compile(ambito)

        if (valorIzquierdo != None and valorDerecho != None): 

            tipo_resultante = self.validar_operacion_aritmetica(valorIzquierdo.type, valorDerecho.type, self.operador) 
            #print ("El tipo seria ====================", tipo_resultante)
            if (tipo_resultante): 
                
                if (self.operador == Operador.POT):
                    print ("este es un codigo 3 direcciones distinto", tipo_resultante)

                    # Cargar parametros base y exponente
                    temp = static_generator.addTemporal() 
                    static_generator.add_exp(temp, 'SP', ambito.size, '+') 
                    # parametro base 
                    static_generator.add_exp(temp, temp, '1', '+') 
                    static_generator.putIntoStack(temp, valorIzquierdo.value)

                    # parametro exponente 
                    static_generator.add_exp(temp, temp, '1', '+') 
                    static_generator.putIntoStack(temp, valorDerecho.value)

                    # Mover el stack pointer, temporalmente 
                    static_generator.newAmbito(ambito.size) 

                    if tipo_resultante == Type.STRING: 
                        print (valorIzquierdo.value)
                        static_generator.load_nativa_potenciaString()
                        static_generator.callFunction('potenciaString')
                    else: 
                        static_generator.load_nativa_potenciaNumerica()  
                        static_generator.callFunction('potenciaNumerica')

                    # recuperar el resultado 
                    resultado = static_generator.addTemporal() 
                    static_generator.getFromStack(resultado, 'SP')

                    # Regresar el stack pointer a donde estaba antes
                    static_generator.returnAmbito(ambito.size)
                    return ReturnCompiler(resultado, tipo_resultante, True)

                else:
                    # Crear el valor tempral para las variables 
                    varTemp = static_generator.addTemporal()        
                    op = self.op_to_string( self.operador)

                    static_generator.add_exp(varTemp, valorIzquierdo.value, valorDerecho.value, op)
                    #print (static_generator.codigo_C3D)
                    return ReturnCompiler( varTemp, tipo_resultante, True)
        return None 

    def validar_operacion_aritmetica(self, left_type, right_type, op):
        
        if op == Operador.PLUS: 
            if (left_type == Type.INT and right_type == Type.INT):  # ENTERO, ENTERO
                return Type.INT
            elif (left_type == Type.FLOAT and right_type == Type.INT):  # FLOAT, ENTERO
                return Type.FLOAT
            elif (left_type == Type.INT and right_type == Type.FLOAT):  # ENTERO, FLOAT
                return Type.FLOAT
            elif (left_type == Type.FLOAT and right_type == Type.FLOAT): # FLOAT, FLOAT
                return Type.FLOAT
            elif (left_type == Type.STRING and right_type == Type.STRING): # STRING, STRING 
                return Type.STRING
            else: 
                print("Error semantico en linea: {}, no se puede Sumar: {} con {}.".format(self.line, left_type, right_type) )
        elif (op == Operador.MINUS):
            if (left_type == Type.INT and right_type == Type.INT):  # ENTERO, ENTERO
                return Type.INT
            elif (left_type ==  Type.INT and right_type == Type.FLOAT): 
                return Type.FLOAT
            elif (left_type == Type.FLOAT and right_type == Type.INT):  
                return Type.FLOAT
            elif (left_type == Type.FLOAT and right_type == Type.FLOAT):  
                return Type.FLOAT
            else: 
                print("Error semantico en linea: {}, no se puede restar: {} con {}.".format(self.line, left_type, right_type) )
        elif (op == Operador.MUL):
            if left_type == Type.INT and right_type == Type.INT:
                return Type.INT
            elif left_type == Type.FLOAT and right_type == Type.INT:
                return Type.FLOAT
            elif left_type == Type.INT and right_type == Type.FLOAT:
                return Type.FLOAT
            elif left_type == Type.FLOAT and right_type == Type.FLOAT:
                return Type.FLOAT
            elif (left_type == Type.STRING and right_type == Type.STRING): # STRING * STRING
                return Type.STRING
            else: 
                print("Error Sintactico en linea {}:, no se puede multiplicar {} con {}.".format(self.line, left_type, right_type) ) 
        elif (op == Operador.DIV):
            if left_type == Type.INT and right_type == Type.INT:
                return Type.FLOAT
            elif left_type == Type.FLOAT and right_type == Type.INT:
                return Type.FLOAT
            elif left_type == Type.INT and right_type == Type.FLOAT:     
                return Type.FLOAT
            elif left_type == Type.FLOAT and right_type == Type.FLOAT:
                return Type.FLOAT
            else: 
                print("Error Sintactico en linea {}:, no se puede dividir {} con {}.".format(self.line, left_type, right_type) ) 
        elif (op == Operador.POT):

            if (  left_type == Type.FLOAT  and right_type == (Type.INT or Type.FLOAT) ):
                return Type.FLOAT
            elif (left_type == Type.INT  and right_type == (Type.INT)):
                return Type.INT
            elif (left_type == Type.INT  and right_type == (Type.FLOAT)):
                return Type.FLOAT
            elif (left_type == Type.STRING  and right_type == (Type.INT)):
                return Type.STRING
            else: 
                msgError = "Error Sintactico en linea {}:, no se puede realizar la potencia de {} con {}.".format(self.line, left_type, right_type)
                static_gen = Generator.C3D_generator
                static_gen.add_comment(msgError)
                print(msgError)

        return None # Si llega aqui, implica que hubo un error 

    def op_to_string (self, operador):

        if operador == Operador.PLUS:
            return "+" 
        elif operador == Operador.MINUS:
            return "-"
        elif operador == Operador.MUL:
            return "*"
        elif operador == Operador.DIV:
            return "/"
            
        
    
