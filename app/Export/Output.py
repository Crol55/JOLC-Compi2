
# Clase para exportar toda la informacion interna del interprete (Mensajes de error, tabla de simbolos, Arbol ast, salida... etc)


def init():
    global errorSintactico 
    global salidaInterprete 
    global AST 

    errorSintactico  = [] # Un arreglo de errores -> Error.py
    salidaInterprete = "" 
    AST              = "" 