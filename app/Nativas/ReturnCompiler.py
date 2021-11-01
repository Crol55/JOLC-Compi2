
class ReturnCompiler: 
    
    def __init__(self, value, type, isTemp, structType=""):
        self.value = value
        self.type = type 
        self.isTemp = isTemp
        # Ayuda con el paso de labels 
        self.trueLabel = "" 
        self.falseLabel = ""
        # ayuda con el tipo compuesto en structs ( ::Ambito )
        self.tipoCompuesto = structType 