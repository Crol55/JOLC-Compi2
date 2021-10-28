
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output
###################
# Proyecto 2 - clases importadas
###################
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator

class While(Instruccion): 
    def __init__(self, expresion:Expresion, sentencias, line, column, nodo):
        Instruccion.__init__(self, line, column)

        self.condicional = expresion 
        self.sentencias  = sentencias 

    def execute(self, ambito):
        #print ("Alguien desea ejecutar lo que contiene este while")

        newAmbito = Ambito(ambito)
        getConditionValue = self.condicional.execute(newAmbito)

        # Verificar que la condicion sea TRUE O FALSE
        if getConditionValue.type == Type.BOOL: 
            
            while getConditionValue.value: # True or false
                
                # Iterar las sentencias del while si existen.
                if self.sentencias != None:

                    ret_sentencias = self.sentencias.execute(newAmbito) # Clase Sentencia.py -> Si retorna algo distinto a None, hay que analizarlo

                    if ret_sentencias != None: # Puede ser un error o (continue, break, return)
                        #print("Una instruccion del while retorno algo?", ret_sentencias)
                        if type(ret_sentencias) == bool: 
                            if ret_sentencias == False: # Hubo un error con alguna instruccion 
                                break
                        elif type(ret_sentencias) == dict:  # RETURN 
                            #print ("Se quiere retornar un valor", type(ret_sentencias))
                            return ret_sentencias
                        elif ret_sentencias.type == Type.BREAK: 
                            #print("se detecto un break")
                            break
                        elif ret_sentencias.type == Type.CONTINUE: # Como 'sentencia.py' se detuvo al encontrar 'continue', lo de abajo por ende ya no se ejecuto
                            #print("Se detecto un continue")
                            pass

                # Verificar una vez mas la condicion del while, si no es Booleano, salirse
                getConditionValue = self.condicional.execute(newAmbito)
                if (getConditionValue.type != Type.BOOL):
                    print ("Error semantico en linea: {}, la condicion debe ser tipo BOOL".format(self.condicional.line))
                    Output.errorSintactico.append( Error("La condicion debe ser tipo BOOL", self.line, self.column) )
                    return 
        else:
            print ("Error semantico en linea: {}, la condicion debe ser tipo BOOL".format(self.condicional.line))
            Output.errorSintactico.append( Error("La condicion debe ser tipo BOOL", self.line, self.column) )
        return 


    ###################
    # Proyecto 2 - codigo abajo
    ###################

    def compile(self, ambito):
        
        temp = Generator() 
        static_gen = temp.getInstance()
        # ===== Inicio while 
        static_gen.add_comment(" INICIO WHILE  ")
        
        continueLabel = static_gen.generarLabel()
        static_gen.save_label(continueLabel)
        # Crear ambito del while y cargar sus etiquetas
        new_ambito = Ambito(ambito)
         
        condicion:ReturnCompiler = self.condicional.compile(new_ambito) # Etiqueta true y false
        new_ambito.continueLabel = continueLabel 
        new_ambito.breakLabel    = condicion.falseLabel
        
        static_gen.save_label(condicion.trueLabel)

        # codigo a ejecutar adentro del while 
        
        self.sentencias.compile(new_ambito)
        # regresar al inicio del while 
        static_gen.add_goto(continueLabel)
        end_label   = condicion.falseLabel
        static_gen.save_label(end_label)
        return 

    