
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

            if (resultado.type == Type.STRUCT):  
                string_concat += self.generar_estructura_para_imprimir_structs(resultado.value)
            else:
                if resultado.type == Type.NULL: #Para que imprima nothing en vez de None

                    resultado.value = "nothing"
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


    def generar_estructura_para_imprimir_structs(self, struct:simbolo): # la impresion del struct tiene una estructura definida (ej. Actor ("calors", 27))
        #print ("Que tipo de variable es ==========================", struct.type)
        string_struct_structure = str (struct.IdSimbolo) + "("
        conta_commas = 0

        for val_atributo in struct.atributos.values(): 
            #print ("wujuuuu", type(val_atributo))
            if conta_commas > 0: 
                string_struct_structure += ", "
            #print ("Sera struct?:", val_atributo.tipoSimbolo)
            if (val_atributo.tipoSimbolo == Type.STRUCT):

                string_struct_structure += self.generar_estructura_para_imprimir_structs(val_atributo.valorSimbolo)
            else:

                string_struct_structure += str(val_atributo.valorSimbolo)
            conta_commas = conta_commas + 1
        string_struct_structure += ")"

        return string_struct_structure
        
        