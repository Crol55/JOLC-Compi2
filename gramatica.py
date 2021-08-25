

'''
    ================== ANALISIS LEXICO ==============================
'''

#Palabras reservadas del lenguaje
rw = { 
    # palabra reservada : TOKEN ASOCIADO
     'Nothing' : 'NOTHING',   
     'Int64'   : 'INT64',    
     'Float64' : 'FLOAT64',  
     'Bool'    : 'BOOL',   
     'Char'    : 'CHAR' ,  
     'String'  : 'STRING',   
     'Arreglos': 'ARRAY',
     'global'  : 'GLOBAL',
     'local'   : 'LOCAL',
     'function': 'FUNCTION',
     'end'     : 'END',
     'true'    : 'TRUE',
     'false'   : 'FALSE',
     'return'  : 'RETURN',
     'if'      : 'IF',
     'elseif'  : 'ELSEIF',
     'else'    : 'ELSE',
     'while'   : 'WHILE',
     'for'     : 'FOR',
     'in'      : 'IN',
     'break'   : 'BREAK',
     'continue': 'CONTINUE',
     'struct'  : 'STRUCT', 
     'mutable' : 'MUTABLE'
}

# Tokens 
tokens = [
    'SUM',
    'RESTA',
    'MUL',
    'DIV',
    'POT',
    'MOD',
    'ENTERO',
    'DECIMAL',
    'IDENTIFICADOR',
    'SEMICOLON',
    'EQUALS',
    'SUFIX',
    'DEQUALS', 
    'GREATER', 'LESSTHAN', 'GEQ','LEQ', 'DIFF',
    'NOT', 'AND', 'OR',
    'LPAR', 'RPAR',
    'STRINGLITERAL', 
    'CHARLITERAL',
    'COMMA', 
    'BRACKETA','BRACKETC'
] + list(rw.values())

# Tokens: Expresiones regulares ( 2 formas -> Expresion regular o Funcion)

# Forma de Expresion regular
t_BRACKETA = r'\['
t_BRACKETC = r']'
t_COMMA = r','
t_CHARLITERAL = r'\'.\''
t_STRINGLITERAL = r'\".*?\"'
t_LPAR = r'\('
t_RPAR = r'\)'
t_DEQUALS = r'=='
t_GREATER = r'>'
t_LESSTHAN = r'<'
t_GEQ = r'>='
t_LEQ = r'<='
t_DIFF = r'!='
t_NOT = r'!'
t_AND = r'&&'
t_OR = r'\|\|'
t_MOD = r'%'
t_POT = r'\^'
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

# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

# Construir el analizador lexico 
import ply.lex as lex 
lexer = lex.lex()

'''
    ===================== ANALISIS SINTACTICO ============================ 
'''

precedence = (
    ('left', 'DEQUALS', 'DIFF'),
    ('left', 'GREATER','LESSTHAN', 'GEQ', 'LEQ'),
    ('left', 'AND', 'OR'),
    ('left', 'SUM', 'RESTA'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('right', 'POT'),
    ('right', 'UMINUS')
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
                   | declareFunction
                   | callFunction
                   | condicional
                   | whileST
                   | forST
                   | struct

    '''
# declareFunction 
def p_declareFunction(t):
    '''declareFunction : FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR returnValue END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR             END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR                  RPAR returnValue END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR                  RPAR             END SEMICOLON
    '''

# returnValue
def p_returnValue(t):
    '''returnValue : RETURN expresion SEMICOLON
                   | RETURN SEMICOLON 
    '''
# lista_parametros
def p_lista_parametros(t):
    '''lista_parametros : lista_parametros COMMA IDENTIFICADOR 
                        | lista_parametros COMMA IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR
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

def p_callFunction(t):
    '''callFunction : IDENTIFICADOR LPAR RPAR SEMICOLON
                    | IDENTIFICADOR LPAR lista_expresion RPAR SEMICOLON
    '''

# condicional
def p_condicional(t):
    '''condicional : IF expresion                   END SEMICOLON
                   | IF expresion elseifList        END SEMICOLON
                   | IF expresion elseifList ELSE   END SEMICOLON
    '''
# elseCond
def p_elseifList(t):
    '''elseifList : elseifList ELSEIF expresion
                  | ELSEIF expresion
    '''
# whileST 
def p_whileST(t):
    '''whileST : WHILE expresion END SEMICOLON
    '''
def p_forST(t):
    '''forST : FOR IDENTIFICADOR IN expresion END SEMICOLON
    '''
# lista_expresion
def p_lista_expresion(t):
    '''lista_expresion : lista_expresion COMMA expresion 
                       | expresion
    '''

#struct 
def p_struct(t):
    '''struct : MUTABLE STRUCT IDENTIFICADOR END SEMICOLON 
              |         STRUCT IDENTIFICADOR END SEMICOLON 
    '''
#expresion
def p_expresion(t):
    '''expresion : RESTA expresion %prec UMINUS 
                 | NOT expresion
                 | expresion AND expresion
                 | expresion OR expresion

                 | expresion SUM expresion 
                 | expresion RESTA expresion
                 | expresion MUL expresion
                 | expresion DIV expresion
                 | expresion POT expresion

                 | expresion DEQUALS expresion
                 | expresion DIFF expresion
                 | expresion GREATER expresion
                 | expresion LESSTHAN expresion
                 | expresion GEQ expresion
                 | expresion LEQ expresion
                 | primitivas
    '''
# primitivas
def p_primitivas(t):
    '''primitivas : ENTERO
                  | DECIMAL
                  | FALSE 
                  | TRUE
                  | STRINGLITERAL
                  | CHARLITERAL
                  | NOTHING
                  | BRACKETA BRACKETC
                  | BRACKETA items BRACKETC
    '''
# items
def p_items(t):
    '''items : items COMMA expresion
             | expresion
    '''
def p_error(t):
    print(t)
    print("Syntax error in input!")


# Construyendo el analizador sintactico 

import ply.yacc as yacc 
parser = yacc.yacc()

file = open('./entrada.jl', 'r')
input = file.read()
#print(input)
parser.parse(input)

