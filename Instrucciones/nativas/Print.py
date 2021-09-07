from Abstractas.Instruccion import Instruccion

class Print(Instruccion): 

    def __init__(self,expresiones, line, column, node, newLine = False):
        
        Instruccion.__init__(self, line, column)
        self.__arreglo_expresiones__ = expresiones
        self.__newLine__ = newLine

    def execute(self, ambito):

        string_concat = ""
        for expresion in self.__arreglo_expresiones__:
            
            resultado = expresion.execute(ambito).value
            string_concat += str(resultado)
        
        # Printear los valores
        if  self.__newLine__:  # println
                #print ("PRINT: ambito en el que estoy al impirmir:",ambito)
                print(string_concat) 
        else: # print
            print(string_concat, end ='') 
        return
        