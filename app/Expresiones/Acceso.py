from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output
from Tabla_Simbolos.Ambito import *
# Proyecto 2 
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator



class Acceso(Expresion): # Clase para acceder a la tabla de simbolos

    def __init__(self,identificador:str, line, column):
        Expresion.__init__(self, line, column)
        self.identificador = identificador


    def execute(self, ambito):
        
        #print ("En que ambito estoy?", ambito.variables)
        #print("Acceso: Que variable debo buscar?", self.identificador)
        valor_variable = ambito.getVariable(self.identificador)
        if valor_variable != None: 
            
         #   print ("ACCESO: tipo y valor de la tabla de simbolos: ",valor_variable.tipoSimbolo, valor_variable.valorSimbolo)
            
            if valor_variable.tipoSimbolo == Type.STRUCT: 
                #print ("Acceso: WHAT?", valor_variable.atributos)
                return Return(Type.STRUCT, valor_variable) 
            #elif valor_variable.tipoSimbolo == Type.ARRAY:
            #    return Return(Type.ARRAY, valor_variable) 
            else: 
                #print ("El paso sera por parametro", valor_variable)
                return Return(valor_variable.tipoSimbolo, valor_variable.valorSimbolo) # Al usar Return () indirectamente utilizamos paso por 'parametros' y no por referencia
        else: 
            print ("Error semantico en linea:{}, La variable:'{}' no existe".format( self.line, self.identificador))
            Output.errorSintactico.append(
                Error("La variable:'{}' no existe".format(self.identificador), self.line, self.column)
            ) 
        return 

        
    def compile(self, ambito:Ambito):
        
        variable_obtenida:simboloC3D = ambito.getVariable(self.identificador)

        if (variable_obtenida): 

            # Instanciar el traductor
            temp = Generator() 
            static_generator = temp.getInstance() 

            static_generator.add_comment("ACCESO a variables")
            # ==== Buscar la variable en heap o stack ====
            # Buscar la variable en el stack
            if (not variable_obtenida.inHeap): 
                print ("search in stack")
                # Temporal donde almacenaremos el dato obtenido del stack
                temporal_C3D = static_generator.addTemporal()

                # ===== Posicion donde se encuentra la variable en el STACK
                pos_in_stack = variable_obtenida.pos 

                if (not variable_obtenida.isStoredGlobally): # La accedemos por posicion relativa
                    pos_in_stack = static_generator.addTemporal() 
                    static_generator.add_exp(pos_in_stack, 'SP', variable_obtenida.pos, '+', " -> posicion relativa")

                static_generator.getFromStack(temporal_C3D, pos_in_stack) 
                # ====== 

                if (variable_obtenida.tipoSimbolo != Type.BOOL):
                    
                    static_generator.add_comment(" FIN ACCESO a variables")
                    return ReturnCompiler(temporal_C3D, variable_obtenida.tipoSimbolo, True, variable_obtenida.structType)
                    
                # tipoSimbolo == Type.BOOL 
                if self.trueLabel == '':
                    self.trueLabel = static_generator.generarLabel()
                if self.falseLabel == '':
                    self.falseLabel = static_generator.generarLabel()
                # agregar if y goto
                static_generator.add_if(temporal_C3D, '1', '==', self.trueLabel)
                static_generator.add_goto(self.falseLabel)
                
                ret =  ReturnCompiler(None, variable_obtenida.tipoSimbolo, False)
                ret.trueLabel  = self.trueLabel 
                ret.falseLabel = self.falseLabel
                static_generator.add_comment(" FIN ACCESO a variables")
                return ret

            else: 
                print ("Search in heap", variable_obtenida.pos, variable_obtenida.tipoSimbolo) # Buscar los datos/variable en el heap
                
                # Temporal donde almacenaremos a que posicion del heap apuntamos desde el stack 
                temporal_C3D = static_generator.addTemporal()
                static_generator.getFromStack(temporal_C3D, variable_obtenida.pos)

                
                static_generator.add_comment(" Fin ACCESO a variables")
                return ReturnCompiler(temporal_C3D, variable_obtenida.tipoSimbolo, True)
                # ====== 
            
        else: 
            print ("variable inexistente")
        return None 

    