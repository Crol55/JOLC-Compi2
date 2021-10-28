

# Clase de proyecto 2 exclusivamente
class simboloC3D():
    
    def __init__(self, idSimbolo, tipoSimbolo, pos, inHeap:bool, isStoredGlobally):
        self.idSimbolo   = idSimbolo
        self.tipoSimbolo = tipoSimbolo
        self.pos         = pos # Indicara en que posicion del stack/heap se encuentra la variable
        self.inHeap      = inHeap # Indicara si debe buscar la variable en el stack o el heap
        self.isStoredGlobally = isStoredGlobally 

        self.valorSimbolo = None # El valor ya no se requiere, ahora se utiliza la posicion
    
