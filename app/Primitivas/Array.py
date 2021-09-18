
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion

class Array(Expresion):
    def __init__(self, lista_expresiones, line, column):
        
        Expresion.__init__(self, line, column)
        self.lista_expresiones = lista_expresiones

    def execute(self, ambito):
        #print("Si llamaron al array para ejecutarse")
        newArray = [] 

        for expresion in self.lista_expresiones: 
            actual_value = expresion.execute(ambito)

            newArray.append( Return(actual_value.type, actual_value.value))
            #print("Encontre una expresion chato", actual_value.type)

        return Return(Type.ARRAY, newArray)