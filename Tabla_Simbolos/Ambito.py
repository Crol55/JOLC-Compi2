
from Tabla_Simbolos.simbolo import simbolo


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
            ambito = self 
            while ambito != None:
                if id_variable in ambito.variables.keys(): # Ya existe en el diccionario del ambito?
                    ambito.variables[id_variable] = new_simbolo # Si ya existe reescribimos el valor (tipado dinamico)
                    return 
                ambito = ambito.ambito_anterior # Si no existe, buscamos en un ambito anterior 
            # Si no lo encontro en ningun ambito, incluyendo el global, debemos insertarlo en el ambito ACTUAL 
            self.variables[id_variable] = new_simbolo


    def getVariable(self, id_variable):
        # Buscar la variable 
        ambito = self 
        while ambito != None: 
            if id_variable in ambito.variables.keys():
                return ambito.variables[id_variable]
            ambito = ambito.ambito_anterior
        return None


    def saveFunction(self, id_function, function, input_line):
        
        if id_function in self.functions.keys():
            print("Error Sintactico en linea",input_line,": La funcion '",id_function,"' ya fue declarada previamente.")
            return False 
        else: 
            self.functions[id_function] = function 
        return True

    def getFunction(self, id_function): 
        ambito = self 
        while ambito != None: 
            if id_function in ambito.functions.keys():
                return ambito.functions[id_function]
            ambito = ambito.ambito_anterior
        return None