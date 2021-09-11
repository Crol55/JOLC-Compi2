
#from Tabla_Simbolos.simbolo import simbolo
from Tabla_Simbolos.simbolo import simbolo

class Ambito():
    def __init__(self, ambito_anterior):
        self.ambito_anterior = ambito_anterior
        self.variables = {}
        self.functions = {}
        self.structs   = {}

    
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
            return False
        
        if id_function in self.functions.keys():
            print("Error Sintactico en linea",input_line,": La funcion '",id_function,"' ya fue declarada previamente.")
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
            print ("Error sintactico en linea: {}, ya existe una Funcion con ese nombre, los structs y funciones no pueden tener el mismo nombre".format(struct.line))
            return False

        if id_struct in self.structs.keys(): 
            print ("Error sintactico en linea: {}, ya existe un Struct con ese nombre declarado previamente".format(struct.line))
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
        