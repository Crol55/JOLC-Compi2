from enum import Enum 
# Tipos de datos nativos del lenguaje
class Type (Enum): 
    NULL   = 0 
    INT    = 1
    FLOAT  = 2
    BOOL   = 3
    ARRAY  = 4
    STRING = 5
    CHAR   = 6
    ANY    = 7
    tipo   = 8
    # PARA INSTRUCCIONES UNICAMENTE (whiel, for, if, funcion..etc)
    RETURNINST   = 9 
    CONTINUE = 10 
    BREAK    = 11

    STRUCT  = 12
    RANGE   = 13