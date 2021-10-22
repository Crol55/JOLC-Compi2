
from typing import List
from Tabla_Simbolos.simbolo import simbolo
from Nativas.Type import Type
from Abstractas.Instruccion import Instruccion
from Export import Output 
# proyecto2 
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler



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
                #print ("Print: falla al nomas entrar", type(expresion), "nose->", resultado.value)
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
                #print("entro aqui por que es un valor puntual")
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
        #print("cuantas veces ingreso", struct.IdSimbolo)
        string_struct_structure = str (struct.IdSimbolo) + "("
        conta_commas = 0

        for val_atributo in struct.atributos.values(): 
            #print ("wujuuuu", type(val_atributo))
            if conta_commas > 0: 
                string_struct_structure += ", "
            
            if (val_atributo.tipoSimbolo == Type.STRUCT):
                #print ("justamente en la 2da pasada fallo")
                string_struct_structure += self.mejorar_presentacion_para_imprimir_structs(val_atributo)
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


    # ======== El codigo de abajo es para el proyecto 2 - C3D (codigo 3 direcciones)

    def compile(self, ambito):
        #print("siu")
        aux_generator = Generator() 
        static_generator = aux_generator.getInstance() 

        static_generator.add_comment("PRINT de datos")

        for expresion in self.__arreglo_expresiones__: 
            
            resultado:ReturnCompiler = expresion.compile(ambito)
            if not resultado: 
                return None
            #print ("Aja->", resultado.type)

            if resultado.type == Type.FLOAT: 
                static_generator.add_print('f', resultado.value, "float64")
            elif resultado.type == Type.INT: 
                static_generator.add_print('d', resultado.value)

            elif resultado.type == Type.BOOL: 
                # Generamos el label de salida
                exitLabel = static_generator.generarLabel() 
                # Parte verdadera
                static_generator.add_label(resultado.trueLabel)
                static_generator.add_print_true() 
                static_generator.add_goto(exitLabel) # evitar entrar a la etiqueta false
                # parte falsa 
                static_generator.add_label(resultado.falseLabel)
                static_generator.add_print_false() 
                static_generator.add_label(exitLabel)# insertamos la etiqueta de salida
                
            elif resultado.type == Type.NULL:
                static_generator.add_print("d", -1)

            elif resultado.type == Type.CHAR:
                #print ("quiay}?", resultado.value)
                static_generator.add_print("c", resultado.value )

            elif (resultado.type == Type.STRING): 
               
                # Cargar la funcion nativa a la salida del compilador para asi poder llamarla despues
                static_generator.load_nativa_printString()
                # como usaremos una funcion, los valores se deben pasar por medio del STACK
                # la funcion printString unicamente recibe un parametro que seria cadena, ej -> printString( cadena )
                print (ambito.size)
                static_generator.add_comment("Iniciamos impresion de strings")
                # Almacenar la posicion del stack en donde inicia nuestra funcion printstring()
                start_of_function = static_generator.addTemporal() # t0
                static_generator.add_exp(start_of_function, 'SP', ambito.size, '+', " Almacenamos el inicio la funcion ") # t0 = SP + size -> aqui iniciara la funcion
                # En la primera posicion almacenaremos el valor de retorno de la funcion, por lo que nos movemos una posicion 
                static_generator.add_comment(" Nos movemos 1 posicion, y aqui sera donde coloquemos el parametro que requiere la funcion printstring()")
                static_generator.add_exp(start_of_function, start_of_function, '1', '+')
                static_generator.putIntoStack(start_of_function, resultado.value) 

                # Mover el stack pointer al inicio de la funcion
                static_generator.add_comment("Inicio de funcion printString()")
                static_generator.newAmbito(ambito.size) # El stack pointer (SP) decide donde inicia la funcion
                # llamando a la funcion generada por static_generator.load_nativa_printString()
                static_generator.callFunction('printString')
                temp_returnValue = static_generator.addTemporal() 
                static_generator.getFromStack(temp_returnValue, 'SP') # El valor de retorno estara en la posicion donde ubicamos el stack pointer (SP)
                # Restaurar el valor del stack pointer
                static_generator.returnAmbito(ambito.size)
                

        if (self.__newLine__):
            static_generator.add_print('c', 10)
                



    

        
        