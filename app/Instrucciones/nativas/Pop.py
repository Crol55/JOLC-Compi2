from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion

class Pop(Instruccion):
    def __init__(self,id_array, line, column, nodo=None):
        
        Instruccion.__init__(self, line, column)
        self.id_array = id_array

    def execute(self, ambito):
        
        # Buscar el array en el ambito
        
        array = ambito.getVariable(self.id_array)
        if array != None: 
            #print("Quieren ejecutar un cagado pop", array.valorSimbolo)
            if array.tipoSimbolo == Type.ARRAY:        
                
                array.valorSimbolo.pop()
                #print ("despues de meterle la info tiene..", len (array.valorSimbolo)) 
            else:
                print ("Error semantico en linea: {}. La variable '{}', no es un ARRAY.".format(self.line, self.id_array))
        else:
            print ("Error semantico en linea: {}. La variable '{}', no existe.".format(self.line, self.id_array))
        return None  


    
        
