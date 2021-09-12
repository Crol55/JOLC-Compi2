
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Instruccion import Instruccion

class Continue(Instruccion):

    def __init__(self, line, column, nodo):
        Instruccion.__init__(self, line, column)
        

    def execute(self, ambito):
        return Return(Type.CONTINUE, None)
    