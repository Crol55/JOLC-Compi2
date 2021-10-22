
from Abstractas.Expresion import *
from Nativas.Return import Return
from Nativas.Type import Type 
# proyecto2 
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator

'''
    Clase para el manejo de valores primitivos 
    * Strings 
    * boolean 
    * char 
    * nothing 
    -------- Los valores primitivos de tipo numerico estan en la clase 'Numerica.py'
'''
class Primitivo(Expresion):
    def __init__(self, rawValue, rawType:Type, line, column):
        Expresion.__init__(self, line, column)

        self.valorPrimitivo = rawValue
        self.tipoDato       = rawType
        #print("val insertado:", rawValue, type(rawValue))


    def execute(self, ambito):        
        objetoRetorno = Return(self.tipoDato, self.valorPrimitivo)
        return objetoRetorno

    def compile(self, ambito):

        aux_gen = Generator() 
        static_generator = aux_gen.getInstance() 
        
        if (self.tipoDato == Type.BOOL):

            # Generar etiquetas solo si estan vacias 
            if self.trueLabel  == '': self.trueLabel  = static_generator.generarLabel() 
            if self.falseLabel == '': self.falseLabel = static_generator.generarLabel()

            if(self.valorPrimitivo):  # == true
                static_generator.add_goto(self.trueLabel)
                static_generator.add_comment("GOTO de abajo, PARA EVITAR ERROR DE GO")
                static_generator.add_goto(self.falseLabel)       
            else: 
                static_generator.add_goto(self.falseLabel)
                static_generator.add_comment("GOTO de abajo, PARA EVITAR ERROR DE GO")
                static_generator.add_goto(self.trueLabel)   

            return_aux = ReturnCompiler(self.valorPrimitivo, self.tipoDato, False) 
            return_aux.trueLabel =  self.trueLabel 
            return_aux.falseLabel = self.falseLabel

            return return_aux
        elif (self.tipoDato == Type.STRING):
            
            static_generator.add_comment(" Inicio Strings")
            # Manejo de string en HEAP 
            inicio_de_string_en_heap = static_generator.addTemporal()    # t0
            static_generator.add_exp(inicio_de_string_en_heap,'H','','') # t0 = H;

            for char in self.valorPrimitivo: 
                #print ("oa:", char)
                static_generator.putIntoHeap( 'H', ord(char) )   # heap[ int(H)] = char
                static_generator.increaseHeapPointer()           # H = H + 1;
            # Fin de cadena
            static_generator.putIntoHeap('H', '-1')              # heap[ int(H)] = -1 
            static_generator.increaseHeapPointer()               # H = H + 1;

            static_generator.add_comment(" Fin Strings")

            self.valorPrimitivo = inicio_de_string_en_heap      # t0

        elif (self.tipoDato == Type.CHAR):
            #print ("que valor primirito tiene: ", self.valorPrimitivo)
            # Convertir el char a integer
            self.valorPrimitivo = ord(self.valorPrimitivo)

        return ReturnCompiler(self.valorPrimitivo, self.tipoDato, False)
        