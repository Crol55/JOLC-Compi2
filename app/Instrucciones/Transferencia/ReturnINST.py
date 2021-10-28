
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Expresion import Expresion
from Abstractas.Instruccion import Instruccion
###################
# Proyecto 2 - clases importadas
###################
from Nativas.ReturnCompiler import ReturnCompiler
from compiler.Generator import Generator


class ReturnINST(Instruccion):
    
    def __init__(self, expresion:Expresion, line, column, nodo):
        Instruccion.__init__(self, line, column)
        self.expresion = expresion 


    def execute(self, ambito):
        
        if self.expresion == None: 
            return {
                "type": Type.RETURNINST, 
                "value": Return(Type.NULL, None) 
            }
        else: 
            valor_a_retornar:Return = self.expresion.execute(ambito)
            return {
                "type": Type.RETURNINST, 
                "value": valor_a_retornar 
            }


    ###################
    # Proyecto 2 - codigo abajo
    ###################

    def compile(self, ambito):
        
        if (ambito.returnLabel == ''): # Si esta vacio implica que se llamo afuera de una funcion
            print ("Error, return afuera de la funcion")
            return None 
            
        temp = Generator()
        static_gen = temp.getInstance()
        static_gen.add_comment(" Inicio - Return")

        # Si se encuentra en una funcion, colocamos el valor del return en la pos 0 de la funcion y hacemos un goto hacia el fin
        if (self.expresion == None): # ej -> return;
            
            static_gen.putIntoStack('SP', '-1')
            
        else: 
            expresion_compilada:ReturnCompiler = self.expresion.compile(ambito) 
            
            if expresion_compilada.type == Type.NULL: 

                static_gen.putIntoStack('SP', '-1')

            elif expresion_compilada.type == Type.BOOL: 
                tempLabel = static_gen.generarLabel() 
                # Parte true
                static_gen.save_label(expresion_compilada.trueLabel)
                static_gen.putIntoStack('SP', '1')
                static_gen.add_goto(tempLabel)
                # Parte false 
                static_gen.save_label(expresion_compilada.falseLabel)
                static_gen.putIntoStack('SP', '0')
                #salida
                static_gen.save_label(tempLabel)
            else: 
                static_gen.putIntoStack('SP', expresion_compilada.value)

            print(expresion_compilada.value)

        static_gen.add_goto(ambito.returnLabel)
        static_gen.add_comment(" FIN - Return ")
        return 
    