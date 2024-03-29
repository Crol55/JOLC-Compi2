
from Nativas.Return import Return
from ..Condicional.Sentencia import Sentencia
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Error import Error
from Export import Output


class For(Instruccion):
    def __init__(self,identificador, expresion, sentencias:Sentencia, line, column, node = None):
        
        Instruccion.__init__(self, line, column)
        self.identificador = identificador 
        self.expresion     = expresion
        self.sentencias    = sentencias

    def execute(self, ambito):
        
        expresion_iterable  = self.expresion.execute(ambito)
        if (expresion_iterable != None ):
            tipo = expresion_iterable.type  
            if (tipo == Type.STRING or tipo == Type.RANGE): 
                self.for_generico(self.identificador, expresion_iterable, self.sentencias, ambito)
            elif (tipo == Type.ARRAY):
                #print("SIUUUUUUUU no pense que fuera a llegar aqui la verdad")
                self.for_arrays(self.identificador, expresion_iterable.value, self.sentencias, ambito)
            #elif (tipo == Type.RANGE):
            #    self.for_string(self.identificador, expresion_iterable.value, self.sentencias, ambito)
            else: 
                print ("Error semantico en linea: {}, el valor a iterar debe ser (STRING, ARRAY o RANGE) y se obtuvo: {}".format(self.line, tipo.name))
                Output.errorSintactico.append(
                Error("El valor a iterar debe ser (STRING, ARRAY o RANGE) y se obtuvo: {}".format(tipo.name), self.line, self.column)
            ) 
        return 


    def for_generico(self, identificador, expresion_iterable:Return, sentencias:Sentencia, ambito): 
        
        newAmbito = Ambito(ambito) # Creamos el ambito del for
        tipo = None 
        if expresion_iterable.type == Type.STRING: 
            tipo = Type.STRING 
        elif expresion_iterable.type == Type.RANGE:
            tipo = Type.INT
        
        for indice in expresion_iterable.value: 
            
            newAmbito.saveVariable(identificador, tipo, indice, 'local')
            #sentencias.execute(newAmbito)

            # Verificar si el for tiene sentencias.
            if self.sentencias != None:

                ret_sentencias = sentencias.execute(newAmbito) # Clase Sentencia.py -> Si retorna algo distinto a None, hay que analizarlo
                
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
                        #print("Se detecto un continue!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        pass
            #print (indice, '-')

    
    def for_arrays(self, identificador, expresion, sentencias:Sentencia, ambito): 
        newAmbito = Ambito(ambito) # Creamos el ambito del for

        for indice in expresion: 
            if indice.type == Type.STRUCT: 
                newAmbito.save_Struct_As_Variable(identificador, 'local', indice.value)
            else: 
                newAmbito.saveVariable(identificador, indice.type, indice.value, 'local')
            #sentencias.execute(newAmbito)

            # Verificar si el for tiene sentencias.
            if self.sentencias != None:

                ret_sentencias = sentencias.execute(newAmbito) # Clase Sentencia.py -> Si retorna algo distinto a None, hay que analizarlo
                
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
                        #print("Se detecto un continue!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        pass

    
    def for_range(): 
        pass 