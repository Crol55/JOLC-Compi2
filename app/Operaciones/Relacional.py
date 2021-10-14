from Nativas.Error import Error
from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from enum import Enum
from Export import Output
# proyecto2 
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler


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
        try: 
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
                #print ("Que estoy comparandn?", resultado_izq.value == resultado_der.value)
            elif this.operador == OperadorRelacional.DISTINT: 
                comparacion.value = resultado_izq.value != resultado_der.value
            return comparacion
        except: 
            #print ("Aparentemente lo de abajo no se ejecuta")
            print("Error sintactico en linea: {}, no se puede operar el tipo {} con el tipo {}"
            .format(this.line, resultado_izq.type, resultado_der.type)) 
            errRelacional = Error ('No se puede utilizar el operador relacional con el tipo {} y tipo {}'
            .format( resultado_izq.type, resultado_der.type), this.line, this.column)

            Output.errorSintactico.append(errRelacional) # Almacenamos el error globalmente
            #print("vamua ver:", errRelacional.descripcion)

    ########## 
    # El codigo de abajo es para el proyecto 2 - C3D (codigo 3 direcciones)
    ##########
    def compile(this, ambito): # El true y false se manejaran como -> 1 y 0
        
        left_exp:ReturnCompiler  = this.left_expresion.compile(ambito) 
        right_exp:ReturnCompiler = this.right_expresion.compile(ambito)

        if (left_exp and right_exp): 
            # Verificar si se puede aplicar la expresion relacional
            boolean = False 
            try: 
                if this.operador == OperadorRelacional.GREATER: 
                    boolean = left_exp.value > right_exp.value 
                elif this.operador == OperadorRelacional.LESS: 
                    boolean = left_exp.value < right_exp.value
                elif this.operador == OperadorRelacional.GEQ: 
                    boolean = left_exp.value >= right_exp.value
                elif this.operador == OperadorRelacional.LEQ: 
                    boolean = left_exp.value <= right_exp.value
                elif this.operador == OperadorRelacional.DEQUAL: 
                    boolean = left_exp.value == right_exp.value
                    #print ("Que estoy comparandn?", left_exp.value == right_exp.value)
                elif this.operador == OperadorRelacional.DISTINT: 
                    boolean = left_exp.value != right_exp.value

                return ReturnCompiler( int(boolean), Type.BOOL, False)
            except: 
                print("Error semantico en linea: {}, no se puede aplicar el operador relacional en el tipo {} con el tipo {}".format(
                    this.line, left_exp.type, right_exp.type)
                )         
        return None 

    
        