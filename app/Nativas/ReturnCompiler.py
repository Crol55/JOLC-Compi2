
class ReturnCompiler: 
    
    def __init__(self, value, type, isTemp):
        self.value = value
        self.type = type 
        self.isTemp = isTemp
        # Ayuda con el paso de labels 
        self.trueLabel = "" 
        self.falseLabel = ""