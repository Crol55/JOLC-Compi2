from Nativas.Type import Type
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, lista_atributos, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        self.lista_idAtributos = lista_atributos #Acceso a variables del struct


    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        #print ("SIUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU", self.identificador, self.id_atributo)
        struct:simbolo = ambito.getVariable(self.identificador)
        #print ("SIUUUUU", len (struct.atributos) )
        if struct != None: 
            # Buscar los atributos adentro del struct
            if self.lista_idAtributos in struct.atributos: 
                
                atribute_simbolo = struct.atributos[self.lista_idAtributos]
                #print ("Que saqueeeeeeeeeeee?", atribute_simbolo.tipoSimbolo, atribute_simbolo.valorSimbolo)
                return Return(atribute_simbolo.tipoSimbolo, atribute_simbolo.valorSimbolo)
            else: 
                print ("Error semantico en linea: {}, el atributo: '{}' no existe en la declaracion del Struct.".format(self.line, self.lista_idAtributos))
                Output.errorSintactico.append(
                    Error("El atributo: '{}' no existe en la declaracion del Struct.".format(self.lista_idAtributos), self.line, self.column)
                ) 
                return False
        else: 
            print ("Error semantico: La variable", self.identificador,"no existe")
            Output.errorSintactico.append(
                Error("La variable: '{}' no existe.".format(self.identificador), self.line, self.column)
            ) 
        return  

    def execute(self, ambito):
        print("Aqui viene el momento decisivo", self.lista_idAtributos)
        struct_temp:simbolo = ambito.getVariable(self.identificador)

        if (struct_temp != None) and (struct_temp.tipoSimbolo == Type.STRUCT):  # creo que esta linea se puede quitar XD
            # Iterar la lista (ej, raton.cola.color.edad)
            for nombre_atributo in self.lista_idAtributos:
                
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
            return Return(struct_temp.tipoSimbolo, struct_temp.valorSimbolo)
        return 
        