from Nativas.Type import Type
from typing import List
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, lista_id_atributos:List, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        #self.id_atributo = lista_id_atributos[0] #Acceso a variables del struct
        self.lista_idAtributo = lista_id_atributos
        

    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        #print ("SIUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU", self.identificador, self.id_atributo)
        #id_del_struct = self.identificador
        struct:simbolo = ambito.getVariable(self.identificador)

        if (struct != None) and (struct.tipoSimbolo == Type.STRUCT): 

            for idAtributo in self.lista_idAtributo: # aqui fijo entra almenos 1 vez..
                
                if struct != None: # verificar que este
                    # Buscar adentro del struct el atributo que deseamos...
                    if idAtributo in struct.atributos: 

                        atributo_simbolo:simbolo = struct.atributos[idAtributo]
                        #print ("Solo entro una maldita vez", atributo_simbolo.atributos)
                        struct = atributo_simbolo  #actualizamos 
            # El resultado de la busqueda puede ser un struct o un valor puntual
            #print ("Que tipe extraje?", struct.tipoSimbolo)
            if struct.tipoSimbolo == Type.STRUCT: 
                return Return(struct.tipoSimbolo, struct) #retorno el struct
            print("ALGUNA VEZ LLEGO ACA ????????????????????????????????")
            return Return(struct.tipoSimbolo, struct.valorSimbolo) #retorno un valor puntual


        return 
        struct:simbolo = ambito.getVariable(self.identificador)
        
        if struct != None: 
            # Buscar los atributos adentro del struct
            if self.id_atributo in struct.atributos: 
                
                atribute_simbolo = struct.atributos[self.id_atributo]
                #print ("Que saqueeeeeeeeeeee?", atribute_simbolo.tipoSimbolo, atribute_simbolo.valorSimbolo)
                return Return(atribute_simbolo.tipoSimbolo, atribute_simbolo.valorSimbolo)
            else: 
                print ("Error semantico en linea: {}, el atributo: '{}' no existe en la declaracion del Struct.".format(self.line, self.id_atributo))
                Output.errorSintactico.append(
                    Error("El atributo: '{}' no existe en la declaracion del Struct.".format(self.id_atributo), self.line, self.column)
                ) 
                return False
        else: 
            print ("Error semantico: La variable", self.identificador,"no existe")
            Output.errorSintactico.append(
                Error("La variable: '{}' no existe.".format(self.identificador), self.line, self.column)
            ) 
        return  
        