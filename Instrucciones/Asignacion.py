
from Nativas.Return import Return
from Abstractas.Instruccion import Instruccion

class Asignacion(Instruccion):
    def __init__(self,tipoVariable,verifyType, id, value, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.nombre_variable = id 
        self.value = value
        self.tipoVariable = tipoVariable
        self.nodo = nodo
        self.verifyType = verifyType
    
    def execute(self, ambito):
        print("tipo ->", self.tipoVariable)
        newValor:Return = self.value.execute(ambito)
        print("El valor que extraje fue:", newValor.value, newValor.type)
        return True
