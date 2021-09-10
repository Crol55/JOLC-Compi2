
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

                if ret != None: # Hubo un error o quiere hacer un (return, break, continue) adentro del if, solo retornamos
                                # Si el retorno es de una funcion, no debemos finalizar la ejecucion de las sentencias de abajo
                    print ("Sentencia: Se encontro algo de caracter especial->", ret) 
                    if type(ret) == dict: 

                        return ret # Solo retornamos que fue lo que ocurrio y las sentencias de abajo dejan de ejecutarse
                    elif (type(ret) == bool and (ret == False)): #Implica que una instruccion esta erronea, por lo que ya no debe seguir ejecutando

                        return False #Retornamos False, para que la clase que llamo a sentencia, sepa que hubo un error
        return 

    
    def check_for_invalid_instructions(self, instruccion):

        if type(instruccion) == Funcion: 
            print ("Error sintactico en linea: {}, una funcion no se puede declarar en este contexto".format(instruccion.line) )
            return True
        return False