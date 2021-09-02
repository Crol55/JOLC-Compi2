# TODAS las nativas, derivan de la interfaz Expresion.py
from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion


class Uppercase(Expresion):
    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito) # Ejecutamos lo que tenga adentro y el resultado debe ser tipo string
        if resultado.type == Type.STRING: 
            resultado_to_upper = resultado.value.upper()
            return Return(Type.STRING, resultado_to_upper)    
        else: 
            print ("Error: Error sintactico, la funcion 'uppercase' no se puede aplicar al tipo de dato:", resultado.type)
        return None




class Lowercase(Expresion):
    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion
        

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito) # Ejecutamos lo que tenga adentro y el resultado debe ser tipo string
        if resultado.type == Type.STRING: 
            resultado_to_lower = resultado.value.lower()
            return Return(Type.STRING, resultado_to_lower)    
        else: 
            print ("Error: Error sintactico, la funcion 'lower' no se puede aplicar al tipo de dato:", resultado.type)
        return None


class typeof(Expresion): # Se comporta como expresion, sin embargo no se puede operar con su valor de retorno
    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion
    
    def execute(self, ambito):
        tipo_dato:Return = self.expresion.execute(ambito)
        #print ("testeo:", tipo_dato.type.name)
        return Return(Type.tipo, tipo_dato.type.name)


