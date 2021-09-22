
from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion

class AccesoArrays(Expresion):
    def __init__(self,id_array, dimensiones, line, column, node=None):
        
        Expresion.__init__(self, line, column)
        self.id_array = id_array
        self.dimensiones = dimensiones


    def execute(self, ambito):
        
        
        array = ambito.getVariable(self.id_array)
        if array != None: 
            #print ("si me estoy ejecutannnndo?", array)
            if array.tipoSimbolo == Type.ARRAY: 
                
                #variable_array = array.valorSimbolo #Obtenemos el array que deseamos iterar
                variable_retorno = Return(Type.ARRAY, array.valorSimbolo)
                # Iteracion de 1 hasta n dimensiones
                # por cada dimension debemos ingresar a un ARRAY 
                for dimension in self.dimensiones: # siempre ingresa, almenos 1 vez

                    val_expresion = dimension.execute(ambito) 

                    if val_expresion.type != Type.INT: 
                        print ("Error semantico en linea: {}. La dimension de un ARRAY debe ser Integer".format(self.line))
                        return None # Nos salimos de la funcion, porque esto es un error
                    # sacar el valor del array (debe ser forzosamente un array)
                    if variable_retorno.type == Type.ARRAY:

                        variable_retorno = variable_retorno.value[val_expresion.value - 1]
                    else: 
                        print ("Error semantico en linea: {}. La dimension que ingreso '{}' no existe en el arreglo".format(self.line, val_expresion.value))
                        return None
                #print("Que vamos a retornar:", variable_retorno.value)
                return variable_retorno

            else: 
               print ("Error semantico en linea: {}. La variable '{}' NO es de tipo ARRAY".format(self.line, self.id_array)) 
        else:
            print ("Error semantico en linea: {}. La variable no existe".format(self.line))
        return 