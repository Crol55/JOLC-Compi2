
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type import Type
from Nativas.Return import Return
from Abstractas.Instruccion import Instruccion
from Nativas.Error import Error
from Export import Output
from .Sentencia import Sentencia
# proyecto2 
from compiler.Generator import Generator
from Nativas.ReturnCompiler import ReturnCompiler



class If(Instruccion): # IF, ELSEIF Y ELSE, tienen un ambito separado

    def __init__(self,expresion, sentencias,elseInst, line, column, node):
        Instruccion.__init__(self, line, column)

        self.condicion = expresion
        self.sentencias = sentencias
        self.else_or_elseif = elseInst # puede ser else (clase sentencia.py) o elseif (clase if.py)
       # print ("Al crear el if", self.condicion.execute(None).value)
       # Agregado en el 2do proyecto
        self.exitIf = '' # Etiqueta de salida para if (Debe ser UNICA) 


    def execute(self, ambito):

        getConditionValue:Return = self.condicion.execute(ambito) 
        #print("Que mierda retorno?", getConditionValue.type)
        if getConditionValue.type == Type.BOOL: 
            
            if getConditionValue.value: #true
                
                if self.sentencias == None: #  No ingresaron sentencias a ejecutar, solo regresamos
                    return 

                # Ejecutamos las instrucciones adentro del if
                newAmbito = Ambito(ambito)
                #print("Aqui tambien se creo un ambito")
                #sff = self.sentencias.execute(newAmbito)
                #print("Adentro del IF ----------------> ", sff)
                #print ("Cuantas instruccines tiene el if", type(self.sentencias))
                return self.sentencias.execute(newAmbito) # PODRIA retornar (return, break,continue)
                 
            elif self.else_or_elseif != None:  
                # Unicamente al else, le creamos aqui el ambito, ya que IF y ELSEIF, crean sus propios ambitos
                if type(self.else_or_elseif) == Sentencia: # Es un ELSE

                    newAmbito = Ambito(ambito)
                    #print("Que carajo hay aqui. aqui se creo un ambito?", self.else_or_elseif)
                    return self.else_or_elseif.execute(newAmbito)  
                # Es un ELSEIF
                return self.else_or_elseif.execute(ambito) 
                     
        else: 
            print ("Error sintactico en linea: {}, la condicion debe ser BOOL y se obtuvo: {}".format(self.line, getConditionValue.type.name))
            Output.errorSintactico.append(
                Error("La condicion debe ser BOOL y se obtuvo: {}".format(getConditionValue.type.name), self.line, self.column)
            ) 
            return False 
        return # El flujo es correcto 


    def compile(self, ambito:Ambito): # Entra a esta clase si es un "IF" o un "Elseif".... si es "else" se va a la clase sentencias.py
        
        temp = Generator() 
        static_gen = temp.getInstance()

        condition:ReturnCompiler = self.condicion.compile(ambito)

        if(condition.type == Type.BOOL):
            # ===== Coloco label true
            static_gen.save_label(condition.trueLabel)

            if self.sentencias != None: # Evaluaremos las sentencias, luego evaluaremos el else
                newAmbito = Ambito(ambito)
                self.sentencias.compile(newAmbito)

            # Tiene un elseif o else -> colocar goto
            if (self.else_or_elseif != None): 
                if (self.exitIf == ''):
                    self.exitIf = static_gen.generarLabel()
                static_gen.add_goto(self.exitIf)
                print ("Cuantas putas veces ingreso?")

            # ==== Coloco label false
            static_gen.save_label(condition.falseLabel)
            
            # ejecutar elseif or else
            if (self.else_or_elseif != None):
                
                self.else_or_elseif.exitIf = self.exitIf # Cumplimos con que sea unica
                self.else_or_elseif.compile(ambito)

            # Colocamos el exitIf -> Solo una vez
            if ( (self.else_or_elseif == None) or (type(self.else_or_elseif) == Sentencia)):
                if (self.exitIf != ''):
                    static_gen.save_label(self.exitIf) 
        else: 
            print ("Error de compilacion en linea: {}, la condicion debe ser BOOL y se obtuvo: {}".format(self.line, condition.type.name))


