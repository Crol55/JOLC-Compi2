
from Instrucciones.Transferencia.Break import Break
from Nativas.Type import Type
from gramatica import interpretar
from Tabla_Simbolos.Ambito import Ambito 


# Aqui se inicia toda la parte de la compilacion 

newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
ast = interpretar()
print("Cantidad de instrucciones: ", ast)
print ("\n")
print (" ================ EXECUTING FROM MAIN.PY ============================")

#try : 
for instruccion in ast: 
    retMain = instruccion.execute(newAmbitoGlobal)
    if retMain != None: # Podria ser un (return, break, o continue) y eso no se permite a menos que este en un loop
        if type(retMain) == bool: 
            print ("Main.py: Una instruccion esta retornando algo distinto a None")
            if retMain == False: # Hubo un error con alguna instruccion 
                print("Main.py: Error en una instruccion: el interprete detuvo la ejecucion")
                break
        elif retMain.type == Type.BREAK: 
            print("Error sintactico: Un 'break' no puede ser declarado afuera de un loop.")
            break
        elif retMain.type == Type.CONTINUE: 
            print("Error sintactico: Un 'continue' no puede ser declarado afuera de un loop.")
            break
#except: 
 #   print("Error Fatal al ejecutar instrucciones")

        
'''
    comandos faltantes: 
    * length
    * for Puede iterar sobre tipos iterables,  (range, arrays, strings)
    * arreglos 
    * Operaciones con arreglos 
    * Gramatica.py linea 351 -> se removio tipo de dato identificador
'''