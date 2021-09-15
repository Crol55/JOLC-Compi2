from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class Parse(Expresion):

    def __init__(self,typeToCast:Type, expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.typeToCast = typeToCast 
        self.expresion  = expresion

    def execute(self, ambito):

        resultado:Return = self.expresion.execute(ambito)
        
        if (resultado.type != Type.STRING): 
            print("Error semantico en linea: {}, la funcion 'Parse' unicamente se puede utilizar con 'STRING' y el parametro recibido fue: {}"
            .format(self.line, resultado.type))
            Output.errorSintactico.append(
                Error("La funcion 'Parse' unicamente se puede utilizar con 'STRING' y el parametro recibido fue: {}".format(resultado.type), self.line, self.column)
            ) 

            return None
        
        if not (self.is_number(resultado.value)):

            print ("Error semantico en linea: {}: El segundo parametro de la funcion 'parse' no es un dato numerico".format(self.line))
            
            Output.errorSintactico.append(
                Error("El segundo parametro de la funcion 'parse' no es un dato numerico".format(resultado.type), self.line, self.column)
            )
            
            return None

        if (self.typeToCast == Type.INT):
            valor_casteado = int(float(resultado.value))
            return Return(Type.INT, valor_casteado)
            
        elif (self.typeToCast == Type.FLOAT):
            valor_casteado = float(resultado.value)
            return Return(Type.FLOAT, valor_casteado)
        else: 
            print ("Error semantico en linea: {}, el primer parametro de la funcion 'parse' debe ser Int64 o Float64 y el parametro enviado fue: {}".format(self.line, self.typeToCast.name))
            Output.errorSintactico.append(
                Error("El primer parametro de la funcion 'parse' debe ser Int64 o Float64 y el parametro enviado fue: {}".format(self.typeToCast.name), self.line, self.column)
            )
        return None


    def is_number(self, cadena_de_texto):
        
        try:
            float(cadena_de_texto)
            return True
        except ValueError:
            return False
        