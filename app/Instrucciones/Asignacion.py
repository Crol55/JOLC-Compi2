
from Tabla_Simbolos.simbolo import simbolo
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Expresion import Expresion
from Nativas.Return import Return
from Nativas.Type   import Type
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output
from Tabla_Simbolos.simboloC3D import simboloC3D
###################
# Imports PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler

class Asignacion(Instruccion):
    def __init__(self, tipoVariable,verifyType, id, value, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.nombre_variable = id 
        self.expresion = value
        self.alcance = tipoVariable
        self.nodo = nodo
        self.verifyType = verifyType
    


    

    def execute(self, ambito:Ambito):

        resultado_expresion:Return = self.expresion.execute(ambito)

        if resultado_expresion.type == self.verifyType or self.verifyType == Type.ANY: 
            
            if resultado_expresion.type == Type.STRUCT: 
                #if resultado_expresion.value.IdSimbolo == 'Contrato':
                #    self.printearlo(resultado_expresion.value)
                ambito.save_Struct_As_Variable(self.nombre_variable, self.alcance, resultado_expresion.value) 
            else: 
                ambito.saveVariable(self.nombre_variable, resultado_expresion.type, resultado_expresion.value, self.alcance)
            
        elif ( type( self.verifyType) == str and resultado_expresion.type == Type.STRUCT ): # ej, raton = nariz::Nariz
            
            if self.verifyType == resultado_expresion.value.IdSimbolo: # struct.tipo == struct.tipo
                ambito.save_Struct_As_Variable(self.nombre_variable, self.alcance, resultado_expresion.value) 
            else: 
                print ("Asignacion: Error semantico en linea: {}. El tipo de dato compuesto: '{}' no coincide con : '{}'".format(self.line, self.verifyType, resultado_expresion.value.IdSimbolo))
        else: 
            print("Error semantico en linea: {}. Los tipos de datos de la variable '{}' no coinciden.".format(self.line, self.nombre_variable))
            Output.errorSintactico.append(
                Error("Los tipos de datos de la variable:{} no coinciden".format(self.nombre_variable), self.line, self.column)
            ) 
        return  # Si returna None, la ejecucion se realizo correctamente


    def printearlo(self, struct:simbolo):
        print ()
        print ()
        print ("********************** PRINTING STRUCT - ASIGNACION **************************") 
        print (struct.IdSimbolo)
        print (struct.atributos)
        print ("id" ,struct.atributos['actor'].IdSimbolo ,struct.atributos['actor'].atributos)
        print ("********************** FIN PRINTING STRUCT - ASIGNACION **************************") 
        print()
        print()

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################

    def compile(self, ambito:Ambito):

        resultado_exp:ReturnCompiler = self.expresion.compile(ambito)

        if (resultado_exp):
            aux_gen = Generator() 
            static_generator = aux_gen.getInstance()
    
            # Inicio de asignacion de variables
            static_generator.add_comment("Asignacion de variables")
            
            
            isStoredInHeap = (resultado_exp.type == (Type.STRING or Type.STRUCT)) 
            simbolo_creado:simboloC3D = ambito.saveVariable_C3D(self.nombre_variable, resultado_exp.type, self.alcance, isStoredInHeap)
            #print ("Que tipo trajo", simbolo_creado.tipoSimbolo)

            # Insertar al stack
            pos_in_stack = simbolo_creado.pos 
            if (not simbolo_creado.isStoredGlobally): 
                pos_in_stack = static_generator.addTemporal() 
                static_generator.add_exp(pos_in_stack, 'SP', simbolo_creado.pos, '+', "    -> Posicion relativa")

            if resultado_exp.type == Type.BOOL: 

                exit_label = static_generator.generarLabel() 
                # colocar etiqueta 
                static_generator.save_label(resultado_exp.trueLabel)
                static_generator.putIntoStack(pos_in_stack, '1')
                static_generator.add_goto(exit_label)
                # colocar 2da etiqueta
                static_generator.save_label(resultado_exp.falseLabel)
                static_generator.putIntoStack(pos_in_stack, '0')
                # Settear la etiqueta de salida
                static_generator.save_label(exit_label)

            else: 
                static_generator.putIntoStack(pos_in_stack, resultado_exp.value)
        
        return