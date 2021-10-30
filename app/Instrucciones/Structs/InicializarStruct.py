
# Esta clase es una clase normal, no hereda de instruccion (Y unicamente es llamada por 'CallFunction.py')
# Esta clase utiliza la clase 'simbolo.py' para crear solo la estructura del struct, y se devuelve, y debe retornar el tipo de dato y el simbolo

from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Nativas.Type import Type
from Instrucciones.Structs.CrearStruct import CrearStruct, Ambito
from Nativas.Error import Error
from Export import Output
###################
# Imports PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from Tabla_Simbolos.simboloC3D import simboloC3D
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator

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

                #print(" *********** InicializarStruct: Que clase esta involucrada: ************", type(parametro_de_inicializacion))
                #print ("Que (tipo) de parametro tiene el prototitpo:", parametro_del_prototipo.tipo)

                if parametro_del_prototipo.tipo != Type.ANY: # Verificamos si tienen el mismo tipo

                    if ( type(parametro_del_prototipo.tipo) == str): # Es un struct
                        
                        struct_simbolo = param_value.value 
                        #print("Encontre un struct: ",parametro_del_prototipo.tipo, ",struct->", type(struct_simbolo) ) 
                        if ( parametro_del_prototipo.tipo != struct_simbolo.IdSimbolo):
                            #print ("Error semantico en linea: {}. El tipo compuesto '{}' no coincide con el enviado: '{}'".format(self.line), param_de_funcion.tipo, struct_simbolo.IdSimbolo)
                            return None 

                    elif parametro_del_prototipo.tipo != param_value.type: 
                        
                        print ("Error Semantico en la linea: {}, los tipos de datos para inicializar el struct no coinciden.".format(self.line))
                        Output.errorSintactico.append( Error(" Los tipos de datos para inicializar el struct no coinciden.", self.line, 0) ) 
                       
                        return False # La funcion retornar con error (False)
                # Ya Puedo almacenar variables adentro del struct
                if type(parametro_del_prototipo.tipo) == str:
                    #print ()
                    #print("Quiero almacenar un struct adentro de otro struct",parametro_del_prototipo.id)
                    #print()
                    nombre_de_variable =  parametro_del_prototipo.id 
                    #struct_anidado = simbolo(nombre_de_variable, param_value.type, None)
                    #struct_anidado.atributos = param_value.value 
                    #self.printearlo (param_value.value)
                    new_struct.atributos[nombre_de_variable] =  param_value.value
                else: 
                    #print ()
                    #print("Quiero almacenar una variable normal adentro del struct")
                    #print()
                    nombre_de_variable =  parametro_del_prototipo.id 
                    new_struct.atributos[nombre_de_variable] =  simbolo(nombre_de_variable, param_value.type, param_value.value)
                #print("Creare la variable", parametro_del_prototipo.id, " Con el tipo de dato ->", parametro_del_prototipo.tipo)
                
            #Depues de crear el struct y sus variables internas, devolvemos el struct
            #print ("pues almenos hasta aqui todo bien no? ==========================================================================================")
            #if new_struct.IdSimbolo == 'Contrato':
            #    actor:simbolo = new_struct.atributos['actor'] 
            #    print ("ah", actor.atributos.atributos)
            #print()
            #print("ABAJO PRINTEO EL STRUCT QUE SE ACABA DE INICIALIZAR")
            #self.printearlo(new_struct)
            return Return(Type.STRUCT, new_struct) 
        else: 
            print("Error semantico en linea: {}, el numero de parametros no coincide con el prototipo del struct.".format(self.line))
            Output.errorSintactico.append(
                Error(" El numero de parametros no coincide con el prototipo del struct.", self.line, 0)
            ) 


    def printearlo(self, struct:simbolo):
        print()
        print()
        print ("********************** PRINTING STRUCT - InicializarStruct **************************") 
        print (struct.IdSimbolo)
        print (struct.atributos)
        print()
        print ("********************** FIN PRINTING STRUCT - InicializarStruct **************************") 
        print()
        


    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################

    def compile (self, ambito:Ambito):  # Solo inserta informacion al HEAP. 
        
        temp = Generator() 
        static_gen = temp.getInstance() 

        static_gen.add_comment(" == Inicializacion de struct ==")
    
        #pos_in_stack = ambito.size # posicion vacia del stack, al almacenar el simboloC3D (en la clase asginacionStruct), el puntero del stack(ambito.size) debe cambiar
        #                           # por esa razon no incrementamos aqui a la siguiente posicion....
        
        TEMP_heapLibre = static_gen.addTemporal()         # t0 
        static_gen.add_exp(TEMP_heapLibre, 'H','','')     # t0 = H;   -> Posicion donde INICIA el struct 

        heap_index = static_gen.addTemporal()   
        static_gen.add_exp(heap_index, TEMP_heapLibre,'','') 
        # Insertar al stack la posicion del heap donde inicia el struct
        #static_gen.putIntoStack(pos_in_stack, heap_index) # stack[ pos ] = H


        new_struct = simboloC3D(self.struct_prototipo.id, Type.STRUCT, TEMP_heapLibre, True, (ambito.ambito_anterior == None) )
        new_struct.isMutable = self.struct_prototipo.isMutable # True or false
          
        # mover el puntero del heap la cantidad de numero de parametros que tenga el struct (para apartar el lugar)
        cantidad_de_params = len (self.struct_prototipo.lista_parametros) 
        static_gen.add_exp('H','H',cantidad_de_params, '+')   # H = H + ( #params)

        # compilar los parametros entrantes y almacenar que posicion tienen respecto a la posicion 0 donde inicia el struct
        posicion_relativa = 0
        conta = 0       # Para no colocar una instruccion de mas
        for parametro_entrante, parametro_del_prototipo in zip(self.parametros, self.struct_prototipo.lista_parametros): 
            
            parametro_compilado:ReturnCompiler = parametro_entrante.compile(ambito) 
            
            # Verificar que tengan el mismo tipado 
            if (parametro_compilado.type == (parametro_del_prototipo.tipo or Type.ANY) ): 
                
                static_gen.putIntoHeap(heap_index, parametro_compilado.value)
                
                if (conta < cantidad_de_params -1):
                    static_gen.add_exp(heap_index, heap_index, 1, '+')              
                
                nombre_atributo = parametro_del_prototipo.id
                new_struct.atributos[nombre_atributo] = simboloC3D(nombre_atributo, parametro_compilado.type, posicion_relativa, True, (ambito.ambito_anterior == None) )

                posicion_relativa = posicion_relativa + 1
                conta = conta + 1
            
            else: 
                msgError = "Error en linea: {}. El tipo de dato no coincide con el prototipo".format(self.line)
                static_gen.add_comment(msgError)
                return None 

        static_gen.add_comment(" == FIN- Inicializacion de struct ==")


        return ReturnCompiler(new_struct, Type.STRUCT, False)
        
        
            
            