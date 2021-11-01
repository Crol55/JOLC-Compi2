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



class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, lista_atributos, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        self.lista_idAtributos = lista_atributos #Acceso a variables del struct


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

    def compile(self, ambito):
        
        auxg = Generator() 
        static_generator = auxg.getInstance() 

        static_generator.add_comment("=== Inicio Acceso Structs ===")

        # Recuperacion de los valores de un struct 
        struct_temporal:simboloC3D = ambito.getVariable(self.identificador)

        # Donde se encuentra el struct en el HEAP? 
        pos_in_heap = static_generator.addTemporal() 
        static_generator.getFromStack(pos_in_heap, struct_temporal.pos)
        # ====
        # En que posicion a partir del inicio del struct se encuentra mi atributo? 

        for nombre_atributo in self.lista_idAtributos:      # la lista puede contener algo como ( Raton.cola.color.atributos...)
            print ("Atributo a buscar:", nombre_atributo)
            if (nombre_atributo in struct_temporal.atributos): 
                
                struct_temporal = struct_temporal.atributos[nombre_atributo]  # El simbolo puede ser un tipo struct o tipo nativo
                print ("pos in heap", struct_temporal.pos)
        
        # Si llega aqui es porque todo estuvo correcto 
        # lugar exacto donde se encuentra el atributo
        static_generator.add_exp(pos_in_heap, pos_in_heap, struct_temporal.pos, '+')
        # ==
        # Obtenemos el valor adentro del heap
        TEMP = static_generator.addTemporal() 
        static_generator.getFromHeap(TEMP, pos_in_heap) # Aqui se encuentra el atributo 
        # == 
        static_generator.add_comment("=== Fin Acceso Structs ===")
        return ReturnCompiler(TEMP, struct_temporal.tipoSimbolo, True) 
        