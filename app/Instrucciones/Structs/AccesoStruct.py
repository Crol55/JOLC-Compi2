from Nativas.Type import Type
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output
###################
# Imports PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler
from Tabla_Simbolos.simboloC3D import simboloC3D
from Instrucciones.Structs.CrearStruct import *


class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, lista_atributos, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        self.lista_idAtributos = lista_atributos #Acceso a atributos del struct


    def printearlo(self, struct:simbolo):
        print ("********************** PRINTING STRUCT - AccesoStruct **************************") 
        print ("********************** PRINTING STRUCT - AccesoStruct **************************") 
        print ("********************** PRINTING STRUCT - AccesoStruct **************************") 
        print ("********************** PRINTING STRUCT - AccesoStruct **************************") 
        print ("********************** PRINTING STRUCT - AccesoStruct **************************") 
        print (struct.IdSimbolo)
        print (struct.atributos)



    def execute(self, ambito):
        print ("Esta se esta ejecuntando?")
        #print("Aqui viene el momento decisivo", self.lista_idAtributos)
        struct_temp:simbolo = ambito.getVariable(self.identificador)
        #self.printearlo(struct_temp)
        #return None

        #if (struct_temp != None) and (struct_temp.tipoSimbolo == Type.STRUCT):  # creo que esta linea se puede quitar XD
        
        for nombre_atributo in self.lista_idAtributos: # Iterar la lista (ej, raton.cola.color.edad)
            #print ("Cuantas veces baja antes de fallar?", struct_temp.IdSimbolo)
            #como esta en un ciclo hay que verificar que no sea None y siempre sea un struct
            if (struct_temp != None) and (struct_temp.tipoSimbolo == Type.STRUCT):
                # Buscar adentro del struct la variable -> puede devolver otro struct o una variable normal
                if nombre_atributo in struct_temp.atributos:
                    
                    struct_temp = struct_temp.atributos[nombre_atributo] # Actualizamos struct_temp
                    
                else: 
                    
                    print ("Error semantico en linea: {}, '{}' no es un atributo del struct '{}'".format(self.line, nombre_atributo, struct_temp.IdSimbolo)) 
                    
                    return None
            else: 
                print ("Error semantico en linea: {}. '{}' no es un struct".format(self.line, struct_temp.IdSimbolo))
                return None
        # Si llega aqui todo esta correcto
        if struct_temp.tipoSimbolo == Type.STRUCT:
            #print ("creo que aqui esta el error", struct_temp.atributos, " que sera?", type(struct_temp.atributos)) 
            return Return(struct_temp.tipoSimbolo, struct_temp)
        else: 
            return Return(struct_temp.tipoSimbolo, struct_temp.valorSimbolo)
        #return 



    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################

    def compile(self, ambito:Ambito):
        
        auxg = Generator() 
        static_generator = auxg.getInstance() 

        static_generator.add_comment("=== Inicio Acceso Structs ===")

        # ============== ACCESO A STRUCT
        struct_temporal:simboloC3D = ambito.getVariable(self.identificador)
        # ==============
        #print ("encontro esta mierda ====================", struct_temporal.tipoSimbolo)
        if ( (struct_temporal != None) and (struct_temporal.tipoSimbolo == Type.STRUCT) ): 

            #print ("Angora??????", struct_temporal.structType)

            # ===== Donde se encuentra el struct en el HEAP? 
            pos_in_heap = static_generator.addTemporal() 
            static_generator.getFromStack(pos_in_heap, struct_temporal.pos)
            # =====

            # En que posicion a partir del inicio del struct se encuentra mi atributo? 
            
            struct_name = struct_temporal.structType # reusable
            pos_of_struct_in_heap = pos_in_heap      # reusable
            parametro_coincidente:Parametro = None   # reusable

            for atributo in self.lista_idAtributos: # cada vez que entre aqui, debe recorrer con un struct sino es un error..
                
                #print ("porque das tanto clavo =======",atributo, struct_name, pos_of_struct_in_heap)
                struct_prototype:CrearStruct= ambito.getStruct( struct_name)
                if (struct_prototype == None):
                    print (f"Error el atributo {atributo} no esta asociado con un struct")
                    return None

                pos_counter = 0
                parametro_coincidente = None
                for parametro in struct_prototype.lista_parametros:
                    if (parametro.id == atributo):
                        #print ("hora de la verga..",parametro.id, parametro.tipoCompuesto)
                        parametro_coincidente = parametro
                        break
                    pos_counter += 1

                if (parametro_coincidente == None): 
                    print (f"Error el atributo {atributo} no existe")
                    return None 
                
                static_generator.add_exp(pos_of_struct_in_heap, pos_of_struct_in_heap, pos_counter, '+', f' -> atributo "{atributo}"')
                static_generator.getFromHeap(pos_of_struct_in_heap, pos_of_struct_in_heap)

                # si reiteramos (tiene mas atributos) 
                #print ("hora de la verga 2..",parametro_coincidente.id, parametro_coincidente.tipoCompuesto)
                struct_name = parametro_coincidente.tipoCompuesto

            ## == 
            static_generator.add_comment("=== Fin Acceso Structs ===")
            print ("aver:",pos_of_struct_in_heap, parametro_coincidente.tipo, True, parametro_coincidente.tipoCompuesto)
            return ReturnCompiler(pos_of_struct_in_heap, parametro_coincidente.tipo, True, parametro_coincidente.tipoCompuesto) 

        else: 
            msgError = "Error al compilar la linea: {}, La variable: {}, no es un struct/No existe".format(self.line, self.identificador)
            print (msgError)
            static_generator.add_comment(msgError)
        