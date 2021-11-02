

# Clase de proyecto 2 exclusivamente
class simboloC3D():
    
    def __init__(self, idSimbolo, tipoSimbolo, pos, inHeap:bool, isStoredGlobally, structName = ""):
        self.idSimbolo   = idSimbolo
        self.tipoSimbolo = tipoSimbolo
        self.pos         = pos # Indicara en que posicion del stack/heap se encuentra la variable
        self.inHeap      = inHeap # Indicara si debe buscar la variable en el stack o el heap
        self.isStoredGlobally = isStoredGlobally 

        self.valorSimbolo = None # El valor ya no se requiere, ahora se utiliza la posicion

        # Exclusivo para structs 
        self.isMutable = False
        self.atributos = {}          # El struct maneja multiples atributos -> no se utiliza en el proyecto 2 
        self.structType = structName # usado en el 2do proyecto
    
