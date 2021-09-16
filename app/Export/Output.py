
# Clase para exportar toda la informacion interna del interprete (Mensajes de error, tabla de simbolos, Arbol ast, salida... etc)


def init():
    global errorSintactico # meter todos los errores, lexicos, sintacticos y semanticos
    global salidaInterprete 
    global AST 
    global tablaSimbolos 

    errorSintactico  = [] # Un arreglo de errores -> Error.py
    salidaInterprete = "" 
    AST              = "" 
    tablaSimbolos    = []