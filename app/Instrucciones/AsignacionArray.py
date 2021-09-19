
from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Tabla_Simbolos.simbolo import simbolo

class AsignacionArray(Instruccion):
    def __init__(self,identificador, dimensiones, expresion, tipo_dato, line, column, nodo=None):
        
        Instruccion.__init__(self, line, column)
        self.id_array = identificador
        self.dimensiones = dimensiones
        self.expresion = expresion
        self.tipo_dato = tipo_dato

    def execute(self, ambito): 
        #actualizar el valor del array existente 

        array:simbolo = ambito.getVariable(self.id_array)
        if array != None:
            if array.tipoSimbolo == Type.ARRAY: 
                #print ("antes de modificarla", array.valorSimbolo)
                array_auxiliar = Return(Type.ARRAY, array.valorSimbolo)
                
                for dim in self.dimensiones: 

                    val_expresion = dim.execute(ambito) 

                    if val_expresion.type != Type.INT: 
                        print ("Error semantico en linea: {}. La dimension de un ARRAY debe ser Integer".format(self.line))
                        return None # Nos salimos de la funcion, porque esto es un error
                    if array_auxiliar.type == Type.ARRAY:
                        # Nos valemos de parametro por referencia que utiliza python para facilitar la actualizacion de un array
                        array_auxiliar = array_auxiliar.value[val_expresion.value] 
                    else: 

                        print ("Error semantico en linea: {}. La dimension que ingreso '{}' no existe en el arreglo".format(self.line, val_expresion.value))
                        return None
                # Al terminar el for, podremos cambiar el valor re-utilizando la variable Return que ya tiene
                nuevo_valor = self.expresion.execute(ambito)

                array_auxiliar.type = nuevo_valor.type 
                array_auxiliar.value = nuevo_valor.value
    
                #print ("Al salirme -> ", array_auxiliar.value)
                #print ("despues de ", array.valorSimbolo)
                    
        return None 
