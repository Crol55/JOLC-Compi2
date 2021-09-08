
from Tabla_Simbolos.Ambito import Ambito
from sys import getcheckinterval
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Instruccion import Instruccion

class If(Instruccion): # IF, ELSEIF Y ELSE, tienen un ambito separado

    def __init__(self,expresion, sentencias,elseInst, line, column, node):
        Instruccion.__init__(self, line, column)

        self.condicion = expresion
        self.sentencias = sentencias
        self.else_or_elseif = elseInst # puede ser else (clase sentencia.py) o elseif (clase if.py)
       # print ("Al crear el if", self.condicion.execute(None).value)


    def execute(self, ambito):

        getConditionValue:Return = self.condicion.execute(ambito) 

        if getConditionValue.type == Type.BOOL: 
            
            if getConditionValue.value: #true
                
                if self.sentencias == None: #  No ingresaron sentencias a ejecutar, solo regresamos
                    return 

                # Ejecutamos las instrucciones adentro del if
                newAmbito = Ambito(ambito)
                #sff = self.sentencias.execute(newAmbito)
                #print("Adentro del IF ----------------> ", sff)
                #print ("Cuantas instruccines tiene el if", type(self.sentencias))
                return self.sentencias.execute(newAmbito) # PODRIA retornar (return, break,continue)
                 
            elif self.else_or_elseif != None:  
                # Ejecutamos las instrucciones adentro del elseif o Else
                newAmbito = Ambito(ambito)
                return self.else_or_elseif.execute(newAmbito)        
        else: 
            print ("Error sintactico en linea: {}, el tipo de dato debe ser BOOL y se obtuvo: {}".format(self.line, getConditionValue.type))

        return False 
