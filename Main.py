from gramatica import interpretar
from Tabla_Simbolos.Ambito import Ambito 
# Aqui se inicia toda la parte de la compilacion 

newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
ast = interpretar()
print("Cantidad de instrucciones: ", ast)

for instruccion in ast: 
    print(instruccion.execute(newAmbitoGlobal))