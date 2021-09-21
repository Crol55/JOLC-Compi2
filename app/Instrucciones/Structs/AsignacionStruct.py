
from Nativas.Type import Type
from Tabla_Simbolos.simbolo import simbolo
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Nativas.Return import Return
from Export import Output

class AsignacionStruct(Instruccion):
    def __init__(self, id_struct, id_atributo, expresion, line, column, node = None):
        
        Instruccion.__init__(self, line, column)
        self.id_struct   = id_struct 
        self.id_atributo = id_atributo # Atributo que el usuario desea modificar
        self.expresion   = expresion


    def execute(self, ambito):
        
        #print (self.id_struct, self.id_atributo)
        # Recuperar el valor a asignar
        valor_a_asignar:Return = self.expresion.execute(ambito)
        
        if (valor_a_asignar != None):

            print ("Cual sera el valor a asignar:", valor_a_asignar.value)
            # Buscar el struct que se quiere actualizar
            struct = ambito.getVariable(self.id_struct)
            #print ("Cual struct estamos buscando", self.id_struct)
            if struct != None: 

                if struct.isMutable:
                    self.actualizar_atributo(struct, valor_a_asignar)
                else: 
                    print("Error semantico en linea: {}, el struct es Inmutable".format(self.line)) 
                    Output.errorSintactico.append(Error("El struct es Inmutable", self.line, self.column)) 

        return
        

    def actualizar_atributo(self, variable_struct, valor_a_asignar):
        
        atributos_de_variable_struct = variable_struct.atributos
        #print("Los atributos son", atributos_de_variable_struct)
        if self.id_atributo in atributos_de_variable_struct: 
            #print ("Hora de tomar un camino", type(valor_a_asignar))
            if valor_a_asignar.type == Type.STRUCT: 
                #print("Struct adentro de un strcut")
                atributos_de_variable_struct[self.id_atributo] = valor_a_asignar.value #Actualizamos el struct
            else: 
                atributo:simbolo = atributos_de_variable_struct[self.id_atributo] # Extraemos el atributo
                #print ("Pues si voy a modificar tu variable jiji XD", atributo.tipoSimbolo, atributo.valorSimbolo)
                atributo.tipoSimbolo  = valor_a_asignar.type 
                atributo.valorSimbolo = valor_a_asignar.value
            #print ("Luego de realizar la actualizacion XD:", atributo.tipoSimbolo, atributo.valorSimbolo)
        else: 
            print ("Error semantico en linea: {}, el atributo '{}' no existe.".format(self.line, self.id_atributo))
            Output.errorSintactico.append(
                Error("El atributo: '{}' no existe.".format(self.id_atributo), self.line, self.column)
            ) 
            