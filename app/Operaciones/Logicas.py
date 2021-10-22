from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from enum import Enum
from Nativas.Error import Error
from Export import Output
# proyecto2 
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler


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
    ########## 
    # El codigo de abajo es para el proyecto 2 - C3D (codigo 3 direcciones)
    ##########

    def compile(this, ambito):
        
        tempGenerator = Generator() 
        static_generator = tempGenerator.getInstance()
        static_generator.add_comment(f"Inicio EXPRESION LOGICA ({this.operador.name})")

        this.checkLabels() # Genero etiqueta: True y False, si y solo si, no existen

        # Cargar etiquetas al lado izquierdo y derecho -> EXP AND EXP
        Label_intermedio_AND_OR = ""

        if (this.operador == OperadorLogico.AND): # Left y right comparten la misma etiqueta false en AND

            Label_intermedio_AND_OR = static_generator.generarLabel() 
            this.left_expresion.trueLabel  = Label_intermedio_AND_OR 
            this.right_expresion.trueLabel = this.trueLabel 
            #compartir etiqueta false
            this.left_expresion.falseLabel = this.right_expresion.falseLabel = this.falseLabel

        elif(this.operador == OperadorLogico.OR): # Comparten la etiqueta true en OR

            Label_intermedio_AND_OR = static_generator.generarLabel()
            this.left_expresion.trueLabel = this.right_expresion.trueLabel = this.trueLabel
            this.left_expresion.falseLabel = Label_intermedio_AND_OR 
            this.right_expresion.falseLabel = this.falseLabel

        
        resultado_izq:ReturnCompiler = this.left_expresion.compile(ambito) 
        static_generator.add_label( Label_intermedio_AND_OR) 
        resultado_der:ReturnCompiler = this.right_expresion.compile(ambito)

        

        if (resultado_izq.type == Type.BOOL and resultado_der.type == Type.BOOL):      

            static_generator.add_comment(f"FIN EXPRESION LOGICA ({this.operador.name})")

            ret_val = ReturnCompiler(None, Type.BOOL, False)
            ret_val.trueLabel = this.trueLabel 
            ret_val.falseLabel = this.falseLabel
            
            return ret_val 
        print ("Error en linea: {}: Los operandos de una operacion logica deben ser tipo 'BOOL'".format(this.line))
        return None 

    def checkLabels (this):
        tempGenerator = Generator() 
        static_generator = tempGenerator.getInstance()
        if this.trueLabel == '':
            this.trueLabel = static_generator.generarLabel() 
        if this.falseLabel == '':
            this.falseLabel = static_generator.generarLabel() 
    
    #def checkLabels(this, resultado_izq:ReturnCompiler):
    #    # Si la expresion de la izquierda es una operacion logica, esta podria haber generado previamente las etiquetas true y false. 
    #    # por lo que hay que verificar, si ya trae sus etiquetas true y false, no crearemos nuevas, sino utilizaremos esas etiquetas
    #    tempGenerator = Generator() 
    #    static_generator = tempGenerator.getInstance()
#
    #    this.trueLabel = resultado_izq.trueLabel
    #    if this.trueLabel == '': # No hay etiqueta 
    #        this.trueLabel = static_generator.generarLabel()
    #    
    #    this.falseLabel = resultado_izq.falseLabel 
    #    if this.falseLabel == '':
    #        this.falseLabel = static_generator.generarLabel()

    ########## 
    # FIN proyecto 2 - C3D (codigo 3 direcciones)
    ##########
        





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
            