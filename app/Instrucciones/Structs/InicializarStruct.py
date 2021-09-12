
# Esta clase es una clase normal, no hereda de instruccion (Y unicamente es llamada por 'CallFunction.py')
# Esta clase utiliza la clase 'simbolo.py' para crear solo la estructura del struct, y se devuelve, y debe retornar el tipo de dato y el simbolo
from types import new_class
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Nativas.Type import Type
from Instrucciones.Structs.CrearStruct import CrearStruct


class InicializarStruct():
    def __init__(self, prototipo:CrearStruct, parametros, line):
        self.struct_prototipo = prototipo # prototipo es el struct como fue Declarado por el usuario
        self.parametros = parametros # son los parametros que el usuario quiere que el strcut tenga al inicializar el struct
        self.line  = line 

    
    def execute(self, ambito):

        new_struct = simbolo(self.struct_prototipo.id, Type.STRUCT, None)
        new_struct.isMutable = self.struct_prototipo.isMutable # True or false

        #Verificar que las variables del prototipo tengan el mismo tipo de dato que los parametros 
        if (len(self.struct_prototipo.lista_parametros) == len(self.parametros)):
            #Verificar que los parametros tengan el tipado correcto requerido por el struct
            # Si el tipado es any, no es necesario verificar
            for (parametro_del_prototipo, parametro_de_inicializacion) in zip(self.struct_prototipo.lista_parametros, self.parametros): 
                #print("tipo de dato:",parametro_del_prototipo.tipo, parametro_del_prototipo.id)
                param_value:Return = parametro_de_inicializacion.execute(ambito)

                if parametro_del_prototipo.tipo != Type.ANY: # Verificamos si tienen el mismo tipo
                    if parametro_del_prototipo.tipo != param_value.type: 
                        print ("Error Sintactico en la linea: {}, los tipos de datos para inicializar el struct no coinciden.".format(self.line))
                        return False # La funcion retornar con error (False)
                print("Creare la variable", parametro_del_prototipo.id)
                nombre_de_variable =  parametro_del_prototipo.id 

                new_struct.atributos[nombre_de_variable] =  simbolo(nombre_de_variable, param_value.type, param_value.value)
            #Depues de crear el struct y sus variables internas, devolvemos el struct
            return Return(Type.STRUCT, new_struct) 
        else: 
            print("Error sintactico en linea: {}, el numero de parametros no coincide con el prototipo del struct.".format(self.line))



    