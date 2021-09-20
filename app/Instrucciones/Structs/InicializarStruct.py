
# Esta clase es una clase normal, no hereda de instruccion (Y unicamente es llamada por 'CallFunction.py')
# Esta clase utiliza la clase 'simbolo.py' para crear solo la estructura del struct, y se devuelve, y debe retornar el tipo de dato y el simbolo
from types import new_class
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Nativas.Type import Type
from Instrucciones.Structs.CrearStruct import CrearStruct
from Nativas.Error import Error
from Export import Output


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
                
                param_value:Return = parametro_de_inicializacion.execute(ambito)

                print("Que clase esta involucrada:", type(parametro_de_inicializacion))
                print ("Que parametro tiene el prototitpo", parametro_del_prototipo.tipo)

                if parametro_del_prototipo.tipo != Type.ANY: # Verificamos si tienen el mismo tipo

                    if ( type(parametro_del_prototipo.tipo) == str): # Es un struct
                        
                        struct_simbolo = param_value.value 
                        print("Encontre un struct",parametro_del_prototipo.tipo, type(struct_simbolo) ) 
                        if ( parametro_del_prototipo.tipo != struct_simbolo.IdSimbolo):
                            #print ("Error semantico en linea: {}. El tipo compuesto '{}' no coincide con el enviado: '{}'".format(self.line), param_de_funcion.tipo, struct_simbolo.IdSimbolo)
                            return None 

                    elif parametro_del_prototipo.tipo != param_value.type: 
                        
                        print ("Error Semantico en la linea: {}, los tipos de datos para inicializar el struct no coinciden.".format(self.line))
                        Output.errorSintactico.append( Error(" Los tipos de datos para inicializar el struct no coinciden.", self.line, 0) ) 
                       
                        return False # La funcion retornar con error (False)
                # Ya Puedo almacenar variables adentro del struct
                if type(parametro_del_prototipo.tipo) == str:
                    print ()
                    print("Quiero almacenar un struct adentro de otro struct")
                    print()
                    nombre_de_variable =  parametro_del_prototipo.id 
                    struct_anidado = simbolo(nombre_de_variable, param_value.type, None)
                    struct_anidado.atributos = param_value.value 

                    new_struct.atributos[nombre_de_variable] =  struct_anidado
                else: 
                    print ()
                    print("Quiero almacenar una variable normal adentro del struct")
                    print()
                    nombre_de_variable =  parametro_del_prototipo.id 
                    new_struct.atributos[nombre_de_variable] =  simbolo(nombre_de_variable, param_value.type, param_value.value)
                print("Creare la variable", parametro_del_prototipo.id, " Con el tipo de dato ->", parametro_del_prototipo.tipo)
                
                #print("QUE LE ALMACENE EN SIMBOLO", param_value.value)
            #Depues de crear el struct y sus variables internas, devolvemos el struct
            print ("pues almenos hasta aqui todo bien no? ==========================================================================================")
            if new_struct.IdSimbolo == 'Contrato':
                actor:simbolo = new_struct.atributos['actor'] 
                print ("ah", actor.atributos.atributos)
            print()
            print()
            return Return(Type.STRUCT, new_struct) 
        else: 
            print("Error semantico en linea: {}, el numero de parametros no coincide con el prototipo del struct.".format(self.line))
            Output.errorSintactico.append(
                Error(" El numero de parametros no coincide con el prototipo del struct.", self.line, 0)
            ) 
            
            