
class simbolo():
    def __init__(self, IdSimbolo, tipoSimbolo, valorSimbolo):
        self.IdSimbolo = IdSimbolo
        self.tipoSimbolo = tipoSimbolo
        self.valorSimbolo = valorSimbolo
        # Solo structs tienen multiples atributos
        self.isMutable = False
        self.atributos = {}

    