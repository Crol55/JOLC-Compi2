
from Nativas.Type import Type
from Tabla_Simbolos.simbolo import simbolo
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Nativas.Return import Return
from Export import Output
###################
# Imports PROYECTO 2 - CODIGO DE 3 DIRECCIONES
###################
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler
from Instrucciones.Structs.CrearStruct import CrearStruct


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
            

    ###################
    # PROYECTO 2 - CODIGO DE 3 DIRECCIONES
    ###################

    def compile(self, ambito):
       
        temp = Generator() 
        static_gen = temp.getInstance() 

        static_gen.add_comment(" ==INICIO - Asignacion de struct==")
        
        new_value:ReturnCompiler = self.expresion.compile(ambito)
        if (new_value != None):

            struct = ambito.getVariable(self.id_struct) 
            if(struct):
                
                struct_prototype:CrearStruct = ambito.getStruct(struct.structType) 
                if struct_prototype.isMutable: 

                    # verificar que el atributo que se desea modificar exista en el prototipo
                    pos_counter = 0
                    existe_atributo = False
                    for parametro in struct_prototype.lista_parametros: 
                        if (parametro.id == self.id_atributo):
                            existe_atributo = True
                            break 
                        pos_counter += 1

                    if (existe_atributo): 
                        # colocar codigo 3 direcciones para modificar el valor 

                        print ("SI existeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", struct.pos, struct.inHeap)
                        
                        # Donde esta el struct en el heap?
                        TEMP_pos_of_struct_in_heap = static_gen.addTemporal() 

                        if (not struct.inHeap):         # implica que hay que buscar la posicion del heap adentro del stack 
                            static_gen.getFromStack(TEMP_pos_of_struct_in_heap, struct.pos)
                        else:                           # Implica que si esta en el heap
                            static_gen.add_exp(TEMP_pos_of_struct_in_heap, struct.pos,'','')

                        # Donde esta el atributo? 
                        static_gen.add_exp(TEMP_pos_of_struct_in_heap, TEMP_pos_of_struct_in_heap, pos_counter, '+')
                        static_gen.putIntoHeap(TEMP_pos_of_struct_in_heap, new_value.value)
                    else: 
                        msgError = "Error en la linea {}, el atributo '{}' no existe".format(self.line, self.id_atributo) 
                        print (msgError)
                        static_gen.add_comment(msgError)
                else:
                    print ("Error el struct es INMUTABLE")
                    static_gen.add_comment(" ===== Error el struct es INMUTABLE =======")
            else:
                print ("Error en linea {}, no existe struct con el nombre: {}".format(self.line, self.id_struct))


        static_gen.add_comment(" == FIN - Asignacion de struct==")
        return