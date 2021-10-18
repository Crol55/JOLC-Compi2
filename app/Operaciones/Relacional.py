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
        ## === PROYECTO 2 
        #this.trueLabel  = "" 
        #this.falseLabel = ""   

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

        temp_generator   = Generator() 
        static_generator = temp_generator.getInstance()

        static_generator.add_comment("Inicio EXPRESION RELACIONAL")
        
        left_exp:ReturnCompiler  = this.left_expresion.compile(ambito) 
        right_exp = None # Ejecutarla despues, solo tiene sentido cuando son Type.BOOL

        ret = ReturnCompiler(None, Type.BOOL, False)

        if (left_exp.type != Type.BOOL): 
            right_exp:ReturnCompiler = this.right_expresion.compile(ambito)
            this.checkLabels()
            if ( (left_exp.type == Type.INT or left_exp.type == Type.FLOAT or left_exp.type == Type.CHAR) and (right_exp.type == Type.INT or right_exp.type == Type.FLOAT or right_exp.type == Type.CHAR) ):

                static_generator.add_if(left_exp.value, right_exp.value, this.op_To_string(), this.trueLabel)
                static_generator.add_goto(this.falseLabel)   
            
        else: # type -> BOOL 
            
            # left expression
            leftTemp = static_generator.addTemporal()
            # parte verdadera
            static_generator.save_label(left_exp.trueLabel)
            static_generator.add_exp(leftTemp, '1', '', '')

            gotoRight = static_generator.generarLabel() # exit to right expresion
            static_generator.add_goto(gotoRight)
            # parte falsa 
            static_generator.save_label(left_exp.falseLabel)
            static_generator.add_exp(leftTemp, '0', '', '')

            static_generator.save_label(gotoRight)
            # Right expression

            right_exp:ReturnCompiler = this.right_expresion.compile(ambito)
            if (right_exp.type != Type.BOOL): 
                print ("Error, en expresion relacional")
                static_generator.add_comment("\t Error en expresion relacional")
                return  None 
            rightTemp = static_generator.addTemporal() # Temporal (t0) donde se almacenara el valor de true o false
            exitLabel = static_generator.generarLabel()
            # parte verdadera
            static_generator.save_label(right_exp.trueLabel) 
            static_generator.add_exp(rightTemp, '1', '', '')
            static_generator.add_goto(exitLabel)
            # parte falsa 
            static_generator.save_label(right_exp.falseLabel) 
            static_generator.add_exp(rightTemp, '0', '', '')
            # colocar la el ultimo label 
            static_generator.save_label(exitLabel)
            # Comparar leftTemp con rightTemp 

            this.checkLabels() 
            static_generator.add_if(leftTemp, rightTemp, this.op_To_string(), this.trueLabel)
            static_generator.add_goto(this.falseLabel)        
                
            

        static_generator.add_comment("FIN EXPRESION RELACIONAL")  

        ret.trueLabel = this.trueLabel 
        ret.falseLabel = this.falseLabel 
        return ret      
        #return None 


    def checkLabels(this):
        tempGenerator = Generator() 
        static_generator = tempGenerator.getInstance()
        if this.trueLabel == '':
            this.trueLabel = static_generator.generarLabel() 
        if this.falseLabel == '':
            this.falseLabel = static_generator.generarLabel() 


    def op_To_string(this):

        if this.operador == OperadorRelacional.GREATER: 
            return '>'
        elif this.operador == OperadorRelacional.LESS: 
            return '<'
        elif this.operador == OperadorRelacional.GEQ: 
            return '>='
        elif this.operador == OperadorRelacional.LEQ: 
            return '<='
        elif this.operador == OperadorRelacional.DEQUAL: 
            return '=='
        elif this.operador == OperadorRelacional.DISTINT: 
            return '!='    
        