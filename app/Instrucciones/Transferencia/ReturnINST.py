
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Abstractas.Instruccion import Instruccion

class ReturnINST(Instruccion):
    
    def __init__(self, expresion:Expresion, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.expresion = expresion 


    def execute(self, ambito):
        
        if self.expresion == None: 
            return {
                "type": Type.RETURNINST, 
                "value": Return(Type.NULL, None) 
            }
        else: 
            valor_a_retornar:Return = self.expresion.execute(ambito)
            return {
                "type": Type.RETURNINST, 
                "value": valor_a_retornar 
            }

    