
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion

class Push(Instruccion):
    def __init__(self,id_array, expresion, line, column, nodo=None):
        
        Instruccion.__init__(self, line, column)
        self.id_array = id_array
        self.expresion = expresion

    def execute(self, ambito):
        
        # Buscar el array en el ambito
        array = ambito.getVariable(self.id_array)
        if array != None: 
            
            if array.tipoSimbolo == Type.ARRAY: 
                
                # verificar que la expresion que se desea almacenar sea valida 
                expr = self.verify_expresion(ambito)
                if expr != None :
                    #print ("antes de meterle la info tiene..", len (array.valorSimbolo)) 
                    array.valorSimbolo.append(expr)
                    #print ("despues de meterle la info tiene..", len (array.valorSimbolo)) 
            else:
                print ("Error semantico en linea: {}. La variable '{}', no es un ARRAY.".format(self.line, self.id_array))
        else:
            print ("Error semantico en linea: {}. La variable '{}', no existe.".format(self.line, self.id_array))
        return None  


    def verify_expresion (self, ambito):
        
        obtener_expresion = self.expresion.execute(ambito)

        if (obtener_expresion != None):
            
            return obtener_expresion 
        return None
        
