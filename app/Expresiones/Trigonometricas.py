
import math
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class Trigonometricas(Expresion):
    def __init__(self, expresion:Expresion, trigonometrica, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion 
        self.operacion_trigonometrica = trigonometrica

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito)
        if (resultado.type == Type.INT or resultado.type == Type.FLOAT): # Solo FLOAT OR INT
            if (resultado.value >= 0 and resultado.value <= (2*math.pi)):
                
                resultado_operacion_trigonometrica = 0
                if (self.operacion_trigonometrica == 'sin'):
                    resultado_operacion_trigonometrica = math.sin(resultado.value)
                elif (self.operacion_trigonometrica == 'cos'):
                    resultado_operacion_trigonometrica = math.cos(resultado.value)
                else:
                    resultado_operacion_trigonometrica = math.tan(resultado.value)
                return Return(Type.FLOAT, resultado_operacion_trigonometrica)
            else:
                print ("Error semantico en linea: {}:. El valor de una funcion trigonometrica '{}' debe estar entre (pi - 2pi) radianes. Y se obtuvo: {}"
                .format(self.line, self.operacion_trigonometrica, resultado.value))

                Output.errorSintactico.append(
                    Error("El valor de una funcion trigonometrica '{}' debe estar entre (pi - 2pi) radianes. Y se obtuvo: {}"
                    .format(self.operacion_trigonometrica, resultado.value), self.line, self.column)
                )
        else: 
            print ("Error semantico en linea: {}:. El parametro de una trigonometrica '{}' debe ser Int64 o Float64 y recibio: {}"
            .format(self.line, self.operacion_trigonometrica, resultado.type.name))    

            Output.errorSintactico.append(
                    Error("El valor de una funcion trigonometrica '{}' debe estar entre (pi - 2pi) radianes. Y se obtuvo: {}"
                    .format(self.operacion_trigonometrica, resultado.value), self.line, self.column)
            )
            
        return 
    
