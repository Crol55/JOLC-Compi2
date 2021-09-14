from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from enum import Enum
from Nativas.Error import Error
from Export import Output


class OperadorLogico(Enum):
    AND = 0
    OR  = 1

class Logicas(Expresion):
    def __init__(this, left_expresion:Expresion, right_expresion:Expresion, operador,  line, column):
        
        Expresion.__init__(this, line, column)
        this.left_expresion = left_expresion
        this.right_expresion = right_expresion
        this.operador = operador

        

    def execute(this, ambito):
        left_result:Return  = this.left_expresion.execute(ambito)
        right_result:Return = this.right_expresion.execute(ambito)

        #print ("Dato izquierdo:", left_result.value)
        operation_state = False
        if(left_result.type == Type.BOOL and right_result.type == Type.BOOL): 
            if this.operador == OperadorLogico.AND:
                operation_state = left_result.value and right_result.value 
            elif this.operador == OperadorLogico.OR: 
                operation_state = left_result.value or right_result.value
            return Return(Type.BOOL, operation_state) 
        else: 
            print ("Error Sintactico en linea: {}: Los operandos de una operacion logica deben ser tipo 'BOOL'".format(this.line))
            Output.errorSintactico.append(Error("Los operandos de una operacion logica deben ser tipo 'BOOL'",this.line, this.column))


class Not (Expresion):
    def __init__(this, expresion:Expresion,  line, column):
        Expresion.__init__(this, line, column)
        this.expresion = expresion
    
    def execute(this, ambito):
        
        resultado_expresion:Return = this.expresion.execute(ambito)
        if resultado_expresion.type == Type.BOOL: 
            valor_negado = not resultado_expresion.value 
            return Return(Type.BOOL, valor_negado)
        else: 
            print ("Error Sintactico en linea: {}: La expresion NOT '!', debe negar un valor BOOL, y se obtuvo: {}" 
            .format(this.line, resultado_expresion.type))
            
            Output.errorSintactico.append(
                Error("La expresion NOT '!', debe negar un valor BOOL, y se obtuvo:".format(resultado_expresion.type),this.line, this.column)
            )

        return 
            