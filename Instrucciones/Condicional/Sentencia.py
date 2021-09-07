
from Instrucciones.Functions.Funcion import Funcion
from Abstractas.Instruccion import Instruccion

class Sentencia(Instruccion):

    def __init__(self,instrucciones, line, column, node):

        Instruccion.__init__(self, line, column)
        self.__arreglo_instrucciones__ = instrucciones

    def execute(self, ambito):

        for instruccion in self.__arreglo_instrucciones__:
              
            # Verificar que no declaren cosas invalidas adentro de la funcion
            if (not self.check_for_invalid_instructions(instruccion)):

                ret = instruccion.execute(ambito)

                if ret != None: # Hubo un error o quiere hacer un (return, break, continue) adentro del if
                    print ("Sentencia: Se encontro algo de caracter especial")
                    return ret 
        return 

    
    def check_for_invalid_instructions(self, instruccion):

        if type(instruccion) == Funcion: 
            print ("Error sintactico en linea: {}, una funcion no se puede declarar en este contexto".format(instruccion.line) )
            return True
        return False