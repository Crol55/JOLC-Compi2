from Abstractas.Instruccion import Instruccion

class Print(Instruccion):

    def __init__(self,expresiones, line, column, node, newLine = False):
        
        Instruccion.__init__(self, line, column)
        self.__arreglo_expresiones__ = expresiones
        self.__newLine__ = newLine

    def execute(self, ambito):

        for expresion in self.__arreglo_expresiones__: 
            print("QUE QUEREEEEEEEEEEEEEEEEEEEEEEEES?",expresion)
        return  
        