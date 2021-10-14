from Abstractas.Expresion import *
from Nativas.Return import Return
from Nativas.Type import Type as type
from Nativas.ReturnCompiler import ReturnCompiler

class Numerica(Expresion):
    def __init__(self, valorNumerico, tipoDato:type, line, column):

        super().__init__(line, column)

        self.valorNumerico = valorNumerico
        self.tipoDato = tipoDato

    def execute(self, ambito):
        objetoRetorno = Return(self.tipoDato, self.valorNumerico)
        return objetoRetorno

    def compile(self, ambito):
        return ReturnCompiler(self.valorNumerico, self.tipoDato, False)
    