
from Instrucciones.Transferencia.Break import Break
from Nativas.Type import Type
from gramatica import interpretar
from Tabla_Simbolos.Ambito import Ambito 
from Export import Output

# leer la entrada 
file = open('../entrada.jl', 'r')
input = file.read()

# Aqui se inicia toda la parte de la compilacion 

newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
ast = interpretar(input)
print("Cantidad de instrucciones: ", ast)
print ("\n")
print (" ================ EXECUTING FROM MAIN2.PY ============================")

Output.init() # Inicio variables globales 
try : 
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
    print ("Lo que esta aqui abajo, sera enviado al frontend.. sin embargo aun no esta completo:")
    print (Output.salidaInterprete)
    print ("Errores leidos", len( Output.errorSintactico) )
except: 
   print("Error Fatal del interprete al ejecutar instrucciones")
   print ("Errores leidos", len( Output.errorSintactico) )

        
'''
    comandos faltantes: 
    pasos: 
    1. graficar errores 
    2. testear archivos de entrada sin arrays 
    3. Gramatica.py linea 351 -> se removio tipo de dato identificador
    4. Agregar los arrays.. 
    * length
    * FOR Puede iterar sobre tipos iterables,  (range, arrays, strings)
    * arreglos 
    * Operaciones con arreglos
'''