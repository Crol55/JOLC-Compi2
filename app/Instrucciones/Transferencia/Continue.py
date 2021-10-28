
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Instruccion import Instruccion
###################
# PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from compiler.Generator import Generator


class Continue(Instruccion):

    def __init__(self, line, column, nodo):
        Instruccion.__init__(self, line, column)
        

    def execute(self, ambito):
        return Return(Type.CONTINUE, None)

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################
    def compile(self, ambito):
        temp = Generator() 
        static_gen = temp.getInstance() 
        # Coloca directamente el goto -> hacia la etiqueta de inicio|continue de un while o un for
        static_gen.add_goto(ambito.continueLabel)
        return
    