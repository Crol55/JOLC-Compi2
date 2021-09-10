from Tabla_Simbolos.simbolo import simbolo
from Nativas.Return import Return
from Abstractas.Expresion import Expresion

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
                print ("Error sintactico en linea: {}, el atributo: '{}' no existe en la declaracion del Struct.".format(self.line, self.id_atributo))
                return False
        else: 
            print ("Error sintactico: La variable", self.identificador,"no existe")
        return  
        