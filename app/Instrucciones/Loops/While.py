
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


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
                            #print ("Se quiere retornar un valor", ret_sentencias['value'].value)
                            return ret_sentencias['value']
                        elif ret_sentencias.type == Type.BREAK: 
                            #print("se detecto un break")
                            break
                        elif ret_sentencias.type == Type.CONTINUE: # Como 'sentencia.py' se detuvo al encontrar 'continue', lo de abajo por ende ya no se ejecuto
                            pass

                # Verificar una vez mas la condicion del while, si no es Booleano, salirse
                getConditionValue = self.condicional.execute(newAmbito)
                if (getConditionValue.type != Type.BOOL):
                    print ("Error semantico en linea: {}, la condicion debe ser tipo BOOL".format(self.condicional.line))
                    Output.errorSintactico.append( Error("La condicion debe ser tipo BOOL", self.line, self.column) )
                    return 
                #print ("No hubieron errores")
                #return 
        else:
            print ("Error semantico en linea: {}, la condicion debe ser tipo BOOL".format(self.condicional.line))
            Output.errorSintactico.append( Error("La condicion debe ser tipo BOOL", self.line, self.column) )
        return 

    