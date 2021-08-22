from Abstractas.Expresion import *
from Nativas.Return import Return

class Numerica(Expresion):
    def __init__(self, valorNumerico, tipoDato:type, line, column):

        super().__init__(line, column)

        self.valorNumerico = valorNumerico
        self.tipoDato = tipoDato

    def execute(self, ambito):
        objetoRetorno = Return(self.tipoDato, self.valorNumerico)
        return objetoRetorno
    