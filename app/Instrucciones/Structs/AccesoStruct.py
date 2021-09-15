from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output


class AccesoStruct(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, id_atributo:str, line, column, node):
        Expresion.__init__(self, line, column)
        self.identificador = identificador
        self.id_atributo = id_atributo #Acceso a variables del struct


    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        #print ("SIUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU", self.identificador, self.id_atributo)
        struct:simbolo = ambito.getVariable(self.identificador)
        #print ("SIUUUUU", len (struct.atributos) )
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
        