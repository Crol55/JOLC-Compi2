
from Instrucciones.Structs.InicializarStruct import InicializarStruct
from Instrucciones.Transferencia.ReturnINST import ReturnINST
from Nativas.Return import Return
from Nativas.Type import Type
from Instrucciones.Functions.Funcion import Funcion
from Abstractas.Instruccion import Instruccion
from Tabla_Simbolos.Ambito  import Ambito
from Nativas.Error import Error
from Export import Output


class CallFunction( Instruccion ): # call struct y call function utilizan la misma clase porque basicamente son lo mismo
    
    def __init__(self, id, parametros, line, column, node):
        Instruccion.__init__(self, line, column)
        self.id_funcion = id 
        self.parametros = parametros



    def execute(self, ambito): # Al llamar una funcion/struct, se le crea un ambito totalmente nuevo
        # Probar con Funcion
        prototype_function:Funcion = ambito.getFunction(self.id_funcion) # Busca la funcion en el  ambito global
        #print ("funcion que estoy buscando,",self.id_funcion, ambito.functions)
        if prototype_function != None: 

            return self.ejecutar_funcion(ambito, prototype_function) 
        
        # Probar con Struct
        struct_prototype = ambito.getStruct(self.id_funcion)

        if struct_prototype != None: 
            newStruct = InicializarStruct(struct_prototype, self.parametros, self.line).execute(ambito)
            #newStruct.execute(ambito)
            #print("Que devuelve del struct?:", newStruct)
            #print (newStruct.IdSimbolo, newStruct.tipoSimbolo, newStruct.isMutable)
            return newStruct # Al retornarla solo tiene sentido si se utiliza adentro de un parametro, o se iguala a otra variable

        # No existe en funcion ni struct......
        print("Error en linea: {}. La Funcion/Struct no existe".format(self.line))
        Output.errorSintactico.append(
            Error("La Funcion/Struct no existe", self.line, self.column)
        ) 
        return False # Si retorna false, hubo un error



    def ejecutar_funcion(self, ambito, funcion_a_ejecutar):
        #print("CUANTAS LLAMADAS HAY A LA FUNCION SUMA=======================================================")
        new_ambito = Ambito(ambito) # Nuevo ambito y se le incrusta su ambito padre 
        #print("Cuantas veces levanto esta instancia", funcion_a_ejecutar)
        # validar que los parametros sean correctos y crear las funciones si todo es correcto 
        
        if self.crear_variables_de_funcion(funcion_a_ejecutar, new_ambito): 

            # Ejecutar las instrucciones que esten internamente en la funcion
           # print ("Cuantas instrucciones tiene esta funcion *---------->", len(funcion_a_ejecutar.instrucciones))
            for inst in funcion_a_ejecutar.instrucciones: 
                
                posible_return_value = inst.execute(new_ambito) # Solo las instrucciones con Error o (return, continue y break) retornan algo

                if posible_return_value != None: # Hubo error (Retorna false) o es una sentencia de transferencia(Retorna dict)

                    if type(posible_return_value) == dict: # from Class ReturnINST -> si es return ya no ejecutar las instrucciones de abajo
                        #valor_a_retornar = posible_return_value['value']
                        #print("Este valor fue devuelto a la funcion que ejecuto=============================",posible_return_value['value'].value)
                        #print ("ALGUN  ME ENVIO UN RETURN ??????", posible_return_value['value'].value)
                       #print ("Que funcion fue?", type(inst))
                        return posible_return_value['value'] # -> Type -> Return()
                    elif (type(posible_return_value) == bool and (posible_return_value == False)): #Implica que una instruccion esta erronea, por lo que ya no debe seguir ejecutando
                        
                        return False #Retornamos False, para que la clase que llamo a la funcion, sepa que hubo un error

            # Si no existe algun return explicito en la funcion, retornar nothing 
            return Return(Type.NULL, None)
        else: 
            return False


    def crear_variables_de_funcion (self, funcion_a_ejecutar, new_ambito):

        if len (funcion_a_ejecutar.parametros) == len (self.parametros): 
               #Verificar que los parametros tengan el tipado correcto requerido por la funcion original
               # Si el tipado es any, no hay necesidad de verificar 
            for (param_de_funcion, param_de_llamada) in zip(funcion_a_ejecutar.parametros, self.parametros):
                
                get_value_from_expresion:Return = param_de_llamada.execute(new_ambito.ambito_anterior)
                
                if param_de_funcion.tipo != Type.ANY: # Verificar el tipado, sino solo crear la variable en el ambito

                    #print ("al ejecutar la funcion que obtengo", param_de_funcion.tipo, get_value_from_expresion.type)

                    if ( type(param_de_funcion.tipo) == str): # Es un struct
                        #print("Encontre un struct") 
                        struct_simbolo = get_value_from_expresion.value 
                        
                        if ( param_de_funcion.tipo != struct_simbolo.IdSimbolo):
                            print ("Error semantico en linea: {}. El tipo compuesto '{}' no coincide con el enviado: '{}'".format(self.line), param_de_funcion.tipo, struct_simbolo.IdSimbolo)
                            return None 
                    elif (param_de_funcion.tipo != get_value_from_expresion.type): # Si los tipos son distintos, es un error

                        print ("Error Sintactico en la linea: {}, los tipos de datos enviados a la funcion no coinciden.".format(self.line))
                        Output.errorSintactico.append(
                            Error("Los tipos de datos enviados a la funcion no coinciden.", self.line, self.column)
                        ) 
                        return False # La funcion retornar con error (False)
                
                #print ("variables a crear:", param_de_funcion.id, get_value_from_expresion.type, get_value_from_expresion.value)
                # Crear en el nuevo ambito, las variables temporales de la funcion, se pasan por valor 
                #print("Que tipos de variable voy a crear", get_value_from_expresion.type)
                if get_value_from_expresion.type == Type.STRUCT: 
                    new_ambito.save_Struct_As_Variable(param_de_funcion.id, 'local', get_value_from_expresion.value)
                else: 
                    new_ambito.saveVariable(param_de_funcion.id, get_value_from_expresion.type, get_value_from_expresion.value, 'local')
            
            return True # El flujo no se interrumpio, todo se genero correctamente
        else: 
            print("Error sintactico en linea: {}, el numero de parametros no coincide con la funcion.".format(self.line))
            Output.errorSintactico.append( 
                Error(" El numero de parametros no coincide con la funcion.", self.line, self.column)
            ) 

    