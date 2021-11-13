
#from Tabla_Simbolos.simbolo import simbolo
from .simbolo import simbolo
from .simboloC3D import simboloC3D
from Nativas.Error import Error
from Export import Output

class Ambito():

    def __init__(self, ambito_anterior): # constructor

        self.ambito_anterior = ambito_anterior
        self.variables = {}
        self.functions = {}
        self.structs   = {}
        # proyecto 2 - Controlar el tamaño actual de variables en el stack
        self.size = 0 
        # Para while y for 
        self.continueLabel = '' 
        self.breakLabel    = ''
        # para funciones
        self.returnLabel    = ''

        if (ambito_anterior != None ):  # Al inicializar jalamos los valores del ambito anterior, excepto si es el ambito global
            self.size          = ambito_anterior.size 
            self.continueLabel = ambito_anterior.continueLabel
            self.breakLabel    = ambito_anterior.breakLabel
            self.returnLabel   = ambito_anterior.returnLabel

         

    
    def saveVariable(self,id_variable,tipo_variable,valor_variable, alcance):
        # Crear un nuevo simbolo asociado a una variable creada 
        new_simbolo = simbolo(id_variable, tipo_variable, valor_variable)

        if alcance == 'local': 
            self.variables[id_variable] =  new_simbolo

        elif alcance == 'global':
            # Buscar el ambito global
           
            ambito = self  
            while True : 
                if (ambito.ambito_anterior == None): # Implica que estamos en el global
                    ambito.variables[id_variable] = new_simbolo
                    break
                ambito = ambito.ambito_anterior
        else :
            # Determinar si ya existe o si hay que crear una nueva
            # La unica forma de acceder al ambito global si estamos en otro ambito es usando 'global' por lo que aqui no se puede
            ambito = self 
            while ambito != None: # Iterar en los ambitos 

                #if ambito.ambito_anterior == None: # No iteramos en el ambito global 
                #    break 
                if id_variable in ambito.variables.keys(): # Ya existe en el diccionario del ambito?
                    ambito.variables[id_variable] = new_simbolo # Si ya existe reescribimos el valor (tipado dinamico)
                    return 
                ambito = ambito.ambito_anterior # Si no existe, buscamos en un ambito anterior 

            # Si no lo encontro en ningun ambito, debemos insertarlo en el ambito ACTUAL 
            self.variables[id_variable] = new_simbolo
        return 


    def saveVariable_C3D(self, id_variable, tipo_variable, alcance:str, inHeap:bool, structName = '' ):

        print ("variable a crear:========== ", id_variable, self.size)
        if (alcance == 'local'): # Utiliza el ambito actual..
            #print ("encontre un local")
            if id_variable in self.variables.keys():

                print ("var existente")
                var_repetida = self.variables[id_variable]
                var_repetida.tipoSimbolo = tipo_variable    # Por si le cambian el tipo (tipado dinamico)
                return var_repetida # Como ya existe solo la enviamos
            else: 
                newSimbolo = simboloC3D(id_variable, tipo_variable, self.size, inHeap, (self.ambito_anterior == None), structName)
                self.size = self.size + 1 
                self.variables[id_variable] = newSimbolo # Insertamos el nuevo simbolo
                return newSimbolo 

        elif (alcance == 'global'): # Ir al ambito global 

            ambito = self  
            while True: 
                if (ambito.ambito_anterior == None): # Implica que estamos en el global
                    if id_variable in self.variables.keys():

                        print ("var existente")
                        var_repetida = ambito.variables[id_variable]
                        var_repetida.tipoSimbolo = tipo_variable    # Por si le cambian el tipo (tipado dinamico)
                        return var_repetida # Como ya existe solo la enviamos
                    else: 
                        newSimbolo = simboloC3D(id_variable, tipo_variable, self.size, inHeap, True , structName)
                        self.size = self.size + 1 
                        ambito.variables[id_variable] = newSimbolo # Insertamos el nuevo simbolo
                        return newSimbolo 
                ambito = ambito.ambito_anterior
        
        elif (alcance == ''): # Buscar en el ambito actual o en todos los anteriores
            
            ambito_aux = self # Ambito actual
            
            while ambito_aux != None: # Iterar en los ambitos 
                
                if id_variable in ambito_aux.variables.keys(): # Si ya existe, solo retornamos el simbolo, pero modificamos su tipo
                    
                    var_repetida = ambito_aux.variables[id_variable]

                    # como python lo pasa por referencia, si modificamos, modificamos el simbolo adentro de "self.variables" 
                    var_repetida.tipoSimbolo = tipo_variable # Por si le cambian el tipo (tipado dinamico)
                    return var_repetida # Como ya existe solo la enviamos

                ambito_aux = ambito_aux.ambito_anterior # No vamos al ambito anterior 

            # Si no lo encontro en ningun ambito la variable, debemos insertarlo en el ambito ACTUAL
            newSimbolo = simboloC3D(id_variable, tipo_variable, self.size, inHeap, (self.ambito_anterior == None), structName)
            self.size = self.size + 1 
            self.variables[id_variable] = newSimbolo  # Insertamos el nuevo simbolo
            return newSimbolo

        return None 



    def getVariable(self, id_variable):
        # Buscar la variable 
        ambito = self 
        while ambito != None: 
            if id_variable in ambito.variables.keys():
                return ambito.variables[id_variable]
            ambito = ambito.ambito_anterior
        return None


    def saveFunction(self, id_function, function, input_line):

        if id_function in self.structs.keys(): 
            print ("Error sintactico en linea: {}, ya existe un Struct con ese nombre. Una funcion y un stuct, no pueden tener el mismo nombre".format(input_line))
            Output.errorSintactico.append( 
                Error("Ya existe un Struct con el nombre: '{}', una funcion y un stuct, no pueden tener el mismo nombre".format(id_function), function.line, function.column) 
            ) 
            return False
        
        if id_function in self.functions.keys():
            print("Error Sintactico en linea",input_line,": La funcion '",id_function,"' ya fue declarada previamente.")
            Output.errorSintactico.append( 
                Error("La funcion con el nombre: '{}' fue declarada previamente".format(id_function), function.line, function.column) 
            ) 
            return False 
        else: 
            self.functions[id_function] = function 
        return


    def getFunction(self, id_function): 
        ambito = self 
        while ambito != None: 
            if id_function in ambito.functions.keys():
                return ambito.functions[id_function]
            ambito = ambito.ambito_anterior
        return None


    def saveStruct (self, id_struct, struct): # ya que funcion y struct, se crean EXACTAMENTE IGUAL, debemos verificar que no exista en ambos lados
        
        if id_struct in self.functions.keys(): 
            print ("Error semantico en linea: {}, ya existe una Funcion con ese nombre, los structs y funciones no pueden tener el mismo nombre".format(struct.line))
            Output.errorSintactico.append( 
                Error(" Ya existe una Funcion con el nombre :'{}', los structs y funciones no pueden tener el mismo nombre".format(id_struct), struct.line, struct.column) 
            ) 
            return False

        if id_struct in self.structs.keys(): 
            print ("Error semantico en linea: {}, ya existe un Struct con ese nombre declarado previamente".format(struct.line))
            Output.errorSintactico.append( 
                Error("Ya existe un Struct con el nombre: '{}' declarado previamente".format(id_struct), struct.line, struct.column) 
            ) 
            
            return False
        else: 
            self.structs[id_struct] = struct  # Si no existe almacenamos el struct
        return 
        

    def getStruct (self,id_struct): 
        # Iterar en todos los ambitos hasta encontrar el struct 
        ambito = self 
        while ambito != None: 
            if id_struct in ambito.structs.keys():
                return ambito.structs[id_struct]
            ambito = ambito.ambito_anterior
        return None


    #def save_Struct_As_Variable_C3D(self, id_variable, alcance, new_simbolo:simboloC3D):
#
    #    if ( alcance == 'local'):       # utiliza el ambito actual
    #        if ( id_variable in self.variables.keys()):             # Esta repetida 
    #            
    #            var_repetida = self.variables[id_variable]
    #            var_repetida.tipoSimbolo = new_simbolo.tipoSimbolo  # tipado dinamico 
    #            return var_repetida
    #        else: # Es nueva
    #            new_simbolo.pos = self.size                         # lugar en el stack, donde estara este struct
    #            self.variables[id_variable] = new_simbolo
    #            self.size = self.size + 1                           #Incrementamos el stack pointer
    #            return new_simbolo                                  # retorna con 'pos' actualizado
#
    #    elif (alcance == 'global'):     # Busca en el ambito global unicamente
#
    #        ambito = self  
    #        while True: 
    #            if (ambito.ambito_anterior == None):        # Implica que estamos en el global
    #                
    #                if id_variable in self.variables.keys():
    #                    print ("var existente")
    #                    var_repetida = ambito.variables[id_variable]
    #                    var_repetida.tipoSimbolo = new_simbolo.tipoSimbolo   # Por si le cambian el tipo (tipado dinamico)
#
    #                    return var_repetida # Como ya existe solo la enviamos
    #                else: 
    #                    new_simbolo.pos = self.size         #lugar en el stack donde estara este struct
    #                    ambito.variables[id_variable] = new_simbolo # Insertamos el nuevo simbolo
    #                    self.size = self.size + 1 
    #                    
    #                    return new_simbolo
    #            ambito = ambito.ambito_anterior
#
    #    elif (alcance == ''):   # Buscar en el ambito actual o en todos los anteriores
#
    #        ambito_aux = self   # Ambito actual
    #        
    #        while ambito_aux != None: # Iterar en los ambitos 
    #            
    #            if id_variable in ambito_aux.variables.keys(): # Si ya existe, solo retornamos el simbolo, pero modificamos su tipo
    #                
    #                var_repetida = ambito_aux.variables[id_variable]
    #                # como python lo pasa por referencia, si modificamos, modificamos el simbolo adentro de "self.variables" 
    #                var_repetida.tipoSimbolo = new_simbolo.tipoSimbolo  # Por si le cambian el tipo (tipado dinamico)
#
    #                return var_repetida                                 # Como ya existe solo la enviamos
#
    #            ambito_aux = ambito_aux.ambito_anterior # No vamos al ambito anterior 
#
    #        # Si no lo encontro en ningun ambito la variable, debemos insertarlo en el ambito ACTUAL
    #        
    #        new_simbolo.pos = self.size
    #        self.variables[id_variable] = new_simbolo  # Insertamos el nuevo struct
    #        self.size = self.size + 1                  #Incrementamos el stack pointer
#
    #        return new_simbolo 
#
    #    return None

    def save_Struct_As_Variable(self, id_variable, alcance, new_simbolo):
        
        if alcance == 'local': 
            self.variables[id_variable] =  new_simbolo

        elif alcance == 'global':
            # Buscar el ambito global
           
            ambito = self  
            while True : 
                if (ambito.ambito_anterior == None): # Implica que estamos en el global
                    ambito.variables[id_variable] = new_simbolo
                    break
                ambito = ambito.ambito_anterior
        else :
            # Determinar si ya existe o si hay que crear una nueva
            # La unica forma de acceder al ambito global si estamos en otro ambito es usando 'global' por lo que aqui no se puede
            ambito = self 
            while ambito != None: # Iterar en los ambitos 

                if ambito.ambito_anterior == None: # No iteramos en el ambito global 
                    break 
                if id_variable in ambito.variables.keys(): # Ya existe en el diccionario del ambito?
                    ambito.variables[id_variable] = new_simbolo # Si ya existe reescribimos el valor (tipado dinamico)
                    return 
                ambito = ambito.ambito_anterior # Si no existe, buscamos en un ambito anterior 
            # Si no lo encontro en ningun ambito, debemos insertarlo en el ambito ACTUAL 
            # El ambito ACTUAL podria ser el global, a pesar de que no se itero ya que era el global
            self.variables[id_variable] = new_simbolo
        return 
        