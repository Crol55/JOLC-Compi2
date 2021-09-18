from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion

class Length(Expresion):
    def __init__(self,expresion, line, column, nodo=None):
        
        Expresion.__init__(self, line, column)
        self.expresion = expresion

    def execute(self, ambito):
        
        #El tipo de la expresion debe ser un array o una cadena
        resultado = self.expresion.execute(ambito)
        if resultado == None: # Hubo un error 
            return None # Retornamos None, para recuperarnos del error

        # Verificar que el resultado sea cadena o Array
        if resultado.type == Type.ARRAY or resultado.type == Type.STRING:
            size = len(resultado.value)
            return Return(Type.INT, size)
        else: 
            print ("Error semantico en linea: {}. La funcion length, unicamente se puede utilizar para ARRAYS O STRINGS".format(self.line))
        return None  

