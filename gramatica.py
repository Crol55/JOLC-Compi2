

'''
    ================== ANALISIS LEXICO ==============================
'''

#Palabras reservadas del lenguaje
rw = { 
     'Nothing' : 'NOTHING',   
     'Int64'   : 'INT64',    
     'Float64' : 'FLOAT64',  
     'Bool'    : 'BOOL',   
     'Char'    : 'CHAR' ,  
     'String'  : 'STRING',   
     'Arreglos': 'ARRAY'
}

# Tokens 
tokens = [
    'SUM',
    'RESTA',
    'MUL',
    'DIV',
    'ENTERO',
    'DECIMAL',
    'IDENTIFICADOR',
    'SEMICOLON',
    'EQUALS',
    'SUFIX'

] + list(rw.values())

# Tokens: Expresiones regulares ( 2 formas -> Expresion regular o Funcion)

# Forma de Expresion regular
t_SUFIX = r'::'
t_SUM   = r'\+'
t_RESTA = r'-'
t_MUL   = r'\*'
t_DIV   = r'/'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_ignore = ' \t\n'

# Forma de Funcion

def t_IDENTIFICADOR(t): 
    r' ([A-Za-z]|_)([0-9]|[A-Za-z]|_)*'
    t.type = rw.get(t.value,'IDENTIFICADOR') # Si es palabra reservada cambia el tipo, Si no, le devuelve su valor anterior que era 'IDENTIFICADOR'
    return t 

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("ERROR IN PARSE TO FLOAT")
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Construir el analizador lexico 
import ply.lex as lex 
lexer = lex.lex()

'''
    ===================== ANALISIS SINTACTICO ============================ 
'''

precedence = (
     ('left', 'SUM', 'RESTA'),
     ('left', 'MUL', 'DIV')
 )
# Definicion de producciones 
def p_inicio(t): 
    'inicio : instrucciones'

def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion 
                     | instruccion
    '''

def p_instruccion(t):
    '''instruccion : asignacion
    '''

def p_asignacion(t):
    '''asignacion : IDENTIFICADOR EQUALS expresion                 SEMICOLON
                  | IDENTIFICADOR EQUALS expresion SUFIX tipo_dato SEMICOLON
    '''

def p_tipo_dato(t):
    '''tipo_dato : INT64 
                | FLOAT64 
                | BOOL 
                | CHAR 
                | STRING 
                | ARRAY 
                | NOTHING  
    '''

def p_expresion(t):
    '''expresion : expresion SUM expresion 
                | expresion RESTA expresion
                | expresion MUL expresion
                | expresion DIV expresion
                | ENTERO
    '''





# Construyendo el analizador sintactico 

import ply.yacc as yacc 
parser = yacc.yacc()

file = open('./entrada.jl', 'r')
input = file.read()
print(input)
parser.parse(input)

