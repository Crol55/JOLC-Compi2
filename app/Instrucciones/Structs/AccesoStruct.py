from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, lista_atributos, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        self.lista_idAtributos = lista_atributos[0] #Acceso a variables del struct


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
        