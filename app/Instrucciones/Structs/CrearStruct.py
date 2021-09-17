

from Instrucciones.Functions.Parametro import Parametro
from Tabla_Simbolos.Ambito import Ambito
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output


class CrearStruct(Instruccion):
    
    def __init__(self, isMutable, id, atributos:Parametro, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.isMutable        = isMutable 
        self.id               = id 
        self.lista_parametros = atributos
        

    def execute(self, ambito:Ambito):  # cuando se cree, uniamente hay que guardarlo en la tabla de simbolos (ambito)
        
        # Si el tipo de dato del atributo no es uno tipo nativo si no es una variable, entonces debemos buscarla en la tabla de simbolos adentro de structs
        existe_el_tipo_compuesto = True # para saber si almacenamos el struct o no
        for parametro in self.lista_parametros: 

            if type(parametro.tipo) == str: #El tipo de dato es un struct (tipo compuesto)
                #print("param ->", parametro.id, parametro.tipo, type(parametro.tipo))
                struct = ambito.getStruct(parametro.tipo) 
                if (not struct): 

                    print ("Error semantico en linea: {}, el tipo de dato compuesto: '{}' NO existe.".format(parametro.line, parametro.tipo))
                    Output.errorSintactico.append( Error(" El tipo de dato compuesto: '{}' NO existe.".format(parametro.tipo), self.line, self.column) ) 
                    existe_el_tipo_compuesto = False
                    

        if (not existe_el_tipo_compuesto):
            return None # retornamos None para que el interprete se recupere del error de esta instruccion. 

        # Almacenamos el struct si pasa la validacion de los tipos compuestos (si es que tiene)
        isStructSaved = ambito.saveStruct(self.id, self) # Almacena esta misma clase adentro de la tabla de simbolos (ambito)
        #isStructSaved # None: Correct, False: Failed 

        return None # retornamos None, para que el interprete se recupere de este error..
