from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion

class Pop(Instruccion):
    def __init__(self,id_array, line, column, nodo=None):
        
        Instruccion.__init__(self, line, column)
        self.expresion = id_array

    def execute(self, ambito):
        
        
        expresionVal:Return = self.expresion.execute(ambito)
        if expresionVal == None: 
            return 

        if expresionVal.type == Type.ARRAY:
            array_to_pop = expresionVal.value # ::List -> Al modificarlo se modificara por referencia

            val_eliminado:Return = array_to_pop.pop()
            return val_eliminado
        else:
            print ("Error semantico en linea: {}. El parametro no es un ARRAY.".format(self.line))
        #array = ambito.getVariable(self.id_array)
        #if array != None: 
        #    #print("Quieren ejecutar un cagado pop", array.valorSimbolo)
        #    if array.tipoSimbolo == Type.ARRAY:        
        #        
        #        val_eliminado:Return = array.valorSimbolo.pop()
        #        #print ("despues de meterle la info tiene..", len (array.valorSimbolo)) 
        #        return val_eliminado
        #    else:
        #        print ("Error semantico en linea: {}. La variable '{}', no es un ARRAY.".format(self.line, self.id_array))
        #else:
        #    print ("Error semantico en linea: {}. La variable '{}', no existe.".format(self.line, self.id_array))
        #return None  


    
        
