
from Tabla_Simbolos.simbolo import simbolo


from Tabla_Simbolos.simbolo import simbolo

class Ambito():
    def __init__(self, ambito_anterior):
        self.ambito_anterior = ambito_anterior
        self.variables = {}
        self.functions = {}
        self.structs   = {}

    
    def saveVariable(self,id_variable,tipo_variable,valor_variable):
        # Crear un nuevo simbolo asociado a una variable creada 
        new_simbolo = simbolo(id_variable, tipo_variable, valor_variable)
        # Determinar si ya existe o si hay que crear una nueva
        ambito = self 
        while ambito != None:
            if id_variable in ambito.variables.keys(): # Ya existe en el diccionario del ambito?
                ambito.variables[id_variable] = new_simbolo # Si ya existe reescribimos el valor (tipado dinamico)
                return 
            ambito = ambito.ambito_anterior # Si no existe, buscamos en un ambito anterior 
        # Si no lo encontro en ningun ambito, incluyendo el global, debemos insertarlo en el ambito ACTUAL 
        self.variables[id_variable] = new_simbolo