
from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion


class Range(Expresion): 
    
    def __init__(self, expresion_izq, expresion_der, line, column):
        
        Expresion.__init__(self, line, column)
        self.expresion_izq = expresion_izq
        self.expresion_der = expresion_der

    def execute(self, ambito):
        
        if (self.expresion_izq != None and self.expresion_der != None): # Si no pasa el if, implica que una expresion tuvo un error 

            left_expresion  = self.expresion_izq.execute(ambito)
            right_expresion = self.expresion_der.execute(ambito)
            
            if (left_expresion.type == Type.INT and right_expresion.type == Type.INT):
                
                if(left_expresion.value <= right_expresion.value):

                    inicio = left_expresion.value 
                    fin = right_expresion.value + 1

                    return Return( Type.RANGE, range(inicio,fin) ) 
                else: 
                    print ("Error semantico en linea: {}. El valor izquierdo de 'Range' debe ser menor al derecho".format(self.line))
            else: 
                print ("Error semantico en linea: {}. El valor para un 'Range' debe ser Integer".format(self.line))
            

        return None