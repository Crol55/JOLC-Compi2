from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion

class Stringcast(Expresion): # convierte cualquier tipo de dato a string

    def __init__(self,expresion:Expresion, line, column):
        
        Expresion.__init__(self, line, column)

        self.expresion  = expresion

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito)
        # castear a string
        string_cast = str(resultado.value)
        #print ("KHA:", resultado.value)
        # Retornar la clase
        return Return(Type.STRING, string_cast)

    
