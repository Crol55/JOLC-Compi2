
from typing import List
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Export import Output 

class Print(Instruccion): 

    def __init__(self,expresiones, line, column, node, newLine = False):
        
        Instruccion.__init__(self, line, column)
        self.__arreglo_expresiones__ = expresiones
        self.__newLine__ = newLine
        

    def execute(self, ambito):

        string_concat = ""
        for expresion in self.__arreglo_expresiones__: 
            
            resultado = expresion.execute(ambito)
            if resultado == None: # Capturamos el error y no imprimimos
                return None 

            if (resultado.type == Type.STRUCT):  
                #print ("DEBERIA ENTRAR 2 VECES !!!!!!!!!!!!!!!!!!!!!!", len(resultado.value.atributos))
                string_concat += self.mejorar_presentacion_para_imprimir_structs(resultado.value)

            elif resultado.type == Type.ARRAY: # Debemos presentar la informacion de una manera leible al usuario
                    string_concat += self.normalizar_impresion_de_arrays(resultado.value)
                    #print("Al terminar la normalizacion obtuve:", string_concat)
                    
            elif resultado.type == Type.BOOL: 
                bool_to_string = str(resultado.value)
                string_concat += bool_to_string.lower()    
                    
            elif resultado.type == Type.NULL: #Para que imprima nothing en vez de None
                string_concat += "nothing"
            else: 
                string_concat += str(resultado.value)
        
        # Printear los valores
        if  self.__newLine__:  # println
                #print ("PRINT: ambito en el que estoy al impirmir:",ambito)
            print(string_concat) 
            Output.salidaInterprete += (string_concat + "\n")  
        else: # print
            print(string_concat, end ='') 
            Output.salidaInterprete += (string_concat + "\n") 
        return


    def mejorar_presentacion_para_imprimir_structs(self, struct:simbolo): # la impresion del struct tiene una estructura definida (ej. Actor ("calors", 27))
        #print ("Que tipo de variable es ==========================", struct.type)
        string_struct_structure = str (struct.IdSimbolo) + "("
        conta_commas = 0

        for val_atributo in struct.atributos.values(): 
            #print ("wujuuuu", type(val_atributo))
            if conta_commas > 0: 
                string_struct_structure += ", "
            
            if (val_atributo.tipoSimbolo == Type.STRUCT):

                string_struct_structure += self.mejorar_presentacion_para_imprimir_structs(val_atributo.valorSimbolo)
            elif val_atributo.tipoSimbolo == Type.ARRAY: 
                #print ("Aqui tiene que estar", val_atributo.valorSimbolo)
                string_struct_structure += self.normalizar_impresion_de_arrays(val_atributo.valorSimbolo)
            elif val_atributo.tipoSimbolo == Type.BOOL: 
                bool_to_string = str(val_atributo.valorSimbolo)
                string_struct_structure += bool_to_string.lower()
            else:

                string_struct_structure += str(val_atributo.valorSimbolo)
            conta_commas = conta_commas + 1
        string_struct_structure += ")"

        return string_struct_structure


    def normalizar_impresion_de_arrays(self, array:List): 
        
        valoresNormalizados = "[" 
        conta_comas = 0
        #print("que longitud tiene ----------------->", len(array))
        for dato_de_array in array: 
           
            if conta_comas > 0: 
                valoresNormalizados += ", "

            if dato_de_array.type == Type.ARRAY: 
                valoresNormalizados += self.normalizar_impresion_de_arrays(dato_de_array.value)
            elif dato_de_array.type == Type.BOOL: 
                bool_to_string = str(dato_de_array.value)
                valoresNormalizados += bool_to_string.lower()
            elif dato_de_array.type == Type.STRUCT: 
                valoresNormalizados += self.mejorar_presentacion_para_imprimir_structs(dato_de_array.value)
            else:
                valoresNormalizados += str(dato_de_array.value)
            
            conta_comas += 1

        valoresNormalizados += "]"
        return valoresNormalizados

        
        