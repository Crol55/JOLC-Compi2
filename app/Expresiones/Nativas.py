# TODAS las nativas, derivan de la interfaz Expresion.py
from Nativas.Return import Return
from Nativas.Type import Type
from Abstractas.Expresion import Expresion
from Nativas.Error import Error
from Export import Output
###################
# Proyecto 2 - clases importadas
###################
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator



class Uppercase(Expresion):

    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito) # Ejecutamos lo que tenga adentro y el resultado debe ser tipo string
        if resultado.type == Type.STRING: 
            resultado_to_upper = resultado.value.upper()
            return Return(Type.STRING, resultado_to_upper)    
        else: 
            print ("Error: Error semantico en linea: {}, la funcion 'uppercase' no se puede aplicar al tipo de dato: {}".format(self.line, resultado.type.name))
            Output.errorSintactico.append(
                Error("La funcion 'uppercase' no se puede aplicar al tipo de dato: {}".format(resultado.type.name), self.line, self.column)
            ) 
        return None

    
    def compile(self, ambito):
        
        temp = Generator()
        static_gen = temp.getInstance()
        static_gen.add_comment(" Inicio - Return")
        ### Calcular el valor
        var_resultante:ReturnCompiler = self.expresion.compile(ambito)

        ### Verificar que sea string
        if (var_resultante.type == Type.STRING):
            
            # Cargar parametro string
            temp = static_gen.addTemporal() 
            static_gen.add_exp(temp, 'SP', ambito.size, '+') 
            # parametro string
            static_gen.add_exp(temp, temp, '1', '+') 
            static_gen.putIntoStack(temp, var_resultante.value)

            # Mover el stack pointer, temporalmente 
            static_gen.newAmbito(ambito.size) 
           
            static_gen.load_nativa_uppercase() 
            static_gen.callFunction('uppercase')
            # recuperar el resultado 
            resultado = static_gen.addTemporal() 
            static_gen.getFromStack(resultado, 'SP')
            # Regresar el stack pointer a donde estaba antes
            static_gen.returnAmbito(ambito.size)
            return ReturnCompiler(resultado, var_resultante.type, True)
        else: 
            pass 
        return None 




class Lowercase(Expresion):
    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion
        

    def execute(self, ambito):
        resultado:Return = self.expresion.execute(ambito) # Ejecutamos lo que tenga adentro y el resultado debe ser tipo string
        if resultado.type == Type.STRING: 
            resultado_to_lower = resultado.value.lower()
            return Return(Type.STRING, resultado_to_lower)    
        else: 
            print ("Error semantico en la linea: {}, la funcion 'lowercase()' no se puede aplicar al tipo de dato:{}".format(self.line, resultado.type.name))
            Output.errorSintactico.append(
                Error("La funcion 'lowercase()' no se puede aplicar al tipo de dato: {}".format(resultado.type.name), self.line, self.column)
            )
        return None

    def compile(self, ambito):
        
        temp = Generator()
        static_gen = temp.getInstance()
        static_gen.add_comment(" Inicio - Return")
        ### Calcular el valor
        var_resultante:ReturnCompiler = self.expresion.compile(ambito)

        ### Verificar que sea string
        if (var_resultante.type == Type.STRING):
            
            # Cargar parametro string
            temp = static_gen.addTemporal() 
            static_gen.add_exp(temp, 'SP', ambito.size, '+') 
            # parametro string
            static_gen.add_exp(temp, temp, '1', '+') 
            static_gen.putIntoStack(temp, var_resultante.value)

            # Mover el stack pointer, temporalmente 
            static_gen.newAmbito(ambito.size) 
           
            static_gen.load_nativa_lowercase() 
            static_gen.callFunction('lowercase')
            # recuperar el resultado 
            resultado = static_gen.addTemporal() 
            static_gen.getFromStack(resultado, 'SP')
            # Regresar el stack pointer a donde estaba antes
            static_gen.returnAmbito(ambito.size)
            return ReturnCompiler(resultado, var_resultante.type, True)
        else: 
            pass 
        return None  


class typeof(Expresion): # Se comporta como expresion, sin embargo no se puede operar con su valor de retorno
    def __init__(self,expresion:Expresion, line, column):
        Expresion.__init__(self, line, column)
        self.expresion = expresion
    
    def execute(self, ambito):
        #print("fijo ingreso no?")
        tipo_dato:Return = self.expresion.execute(ambito)
        #print ("testeo:", tipo_dato.type.name)
        #return Return(Type.tipo, tipo_dato.type.name)
        return Return(Type.tipo, self.enmascarar_tipos_de_datos(tipo_dato.type))


    def enmascarar_tipos_de_datos(self, tipo_dato): # Se enmascaran para presentarselos al usuario 
        tipo_dato_enmascarado = "undefined"
        if tipo_dato == Type.INT: 
            tipo_dato_enmascarado = "Int64"
        elif tipo_dato == Type.FLOAT: 
            tipo_dato_enmascarado = "Float64" 
        elif tipo_dato == Type.NULL: 
            tipo_dato_enmascarado = "nothing"
        elif tipo_dato == Type.BOOL: 
            tipo_dato_enmascarado = "Bool"
        elif tipo_dato == Type.ARRAY: 
            tipo_dato_enmascarado = "Array"
        elif tipo_dato == Type.STRING: 
            tipo_dato_enmascarado = "String"
        elif tipo_dato == Type.CHAR: 
            tipo_dato_enmascarado = "Char"
        elif tipo_dato == Type.tipo: 
            tipo_dato_enmascarado = "Type"
        elif tipo_dato == Type.STRUCT: 
            tipo_dato_enmascarado = "Struct"
        elif tipo_dato == Type.RANGE: 
            tipo_dato_enmascarado = "Range"
        return tipo_dato_enmascarado
