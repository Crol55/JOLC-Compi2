

from Nativas.Type import Type
from Primitivas.Numerica import Numerica
from Primitivas.Primitivo import Primitivo
from Operaciones.Aritmeticas import Aritmeticas,Operador
from Instrucciones.Asignacion import Asignacion
from Expresiones.Nativas import *
from Expresiones.Parse   import *
from Expresiones.Trunc   import *
'''
    ================== ANALISIS LEXICO ==============================
'''

#Palabras reservadas del lenguaje
rw = {
    # palabra reservada : TOKEN ASOCIADO
    'nothing' : 'NOTHING',   
    'Int64'   : 'INT64',    
    'Float64' : 'FLOAT64',  
    'Bool'    : 'BOOL',   
    'Char'    : 'CHAR' ,  
    'String'  : 'STRING',   
    'Arreglo' : 'ARRAY',
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
    'mutable' : 'MUTABLE',
    'log10'   : 'LOG10',
    'log'     : 'LOG',
    'sin'     : 'SENO',
    'cos'     : 'COSENO',
    'tan'     : 'TANGENTE',
    'sqrt'    : 'RAIZ',
    'uppercase':'UPPERCASE',
    'lowercase':'LOWERCASE',
    'print'    : 'PRINT',
    'println'  : 'PRINTLN',
    'parse'  : 'PARSE',
    'trunc'  : 'TRUNC',
    'float'  : 'FLOATCAST',
    'string' : 'STRINGCAST',
    'typeof' : 'TYPEOF',
    'push!'  : 'PUSH',
    'pop!'   : 'POP',
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
    'BRACKETA','BRACKETC', 
    'PUNTO'
] + list(rw.values())

# Tokens: Expresiones regulares ( 2 formas -> Expresion regular o Funcion)

# Forma de Expresion regular
t_PUNTO = r'\.'
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
t_ignore = ' \t'

# Forma de Funcion

# count new lines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
# MLCOMMENT
def t_MLCOMMENT(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count("\n")
# OLCOMMENT
def t_OLCOMMENT(t):
    r'\#.*'
    t.lexer.lineno += 1

def t_IDENTIFICADOR(t): 
    r' ([A-Za-z]|_)([0-9]|[A-Za-z]|_|[!])*'
    t.type = rw.get(t.value,'IDENTIFICADOR') # Si es palabra reservada cambia el tipo, Si no, le devuelve su valor anterior que era 'IDENTIFICADOR'
    if t.type == 'IDENTIFICADOR' and t.value.count('!') > 0:
        t.type = 'error' 
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

    print("Cantidad de instrucciones: ", (t[1]))
    #for ins in t[1]: 
    #    print(ins.execute(None))

def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion 
                     | instruccion
    '''
    if len(t) == 3:
        #print(type(t[1]))
        arr:list = t[1]
        arr.append(t[2])
        t[0] = arr
    else: # Aqui se crea el arreglo que contendra todas las instrucciones a realizar por el lenguaje
        newArray = [] 
        newArray.append( t[1] )
        #t[0] = { "valor": newArray, "tree":"null"} 
        t[0] = newArray
        

def p_instruccion(t):
    '''instruccion : asignacion
                   | asignacion_struct
                   | declareFunction
                   | callFunction 
                   | condicional
                   | whileST
                   | forST
                   | struct 
                   | inst_nativa
    '''
    if t.slice[1].type == 'asignacion':
        #t[0] = { "valor": t[1]['valor'], "tree":"null"}
        t[0] = t[1]

# declareFunction -> | FUNCTION IDENTIFICADOR LPAR                  RPAR lista_instrucciones   SEMICOLON

def p_declareFunction(t):
    '''declareFunction : FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR lista_instrucciones  END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR                  RPAR                      END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR                  RPAR lista_instrucciones  END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR                      END SEMICOLON
    '''
# lista_instrucciones
def p_lista_instrucciones(t):
    '''lista_instrucciones : lista_instrucciones instruccion
                           | lista_instrucciones transferencia
                           | instruccion
                           | transferencia
    '''
# transferencia
def p_transferencia(t):
    '''transferencia : BREAK SEMICOLON
                     | CONTINUE SEMICOLON
                     | returnValue SEMICOLON
    '''
# returnValue
def p_returnValue(t):
    '''returnValue : RETURN expresion 
                   | RETURN 
    '''
# lista_parametros
def p_lista_parametros(t):
    '''lista_parametros : lista_parametros COMMA IDENTIFICADOR 
                        | lista_parametros COMMA IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR
    ''' 
def p_asignacion(t): # La que tiene SUFIX -> Es una declaracion, por lo que no requiere local ni global
    '''asignacion :              IDENTIFICADOR EQUALS expresion                 SEMICOLON
                  | tipoVariable IDENTIFICADOR EQUALS expresion                 SEMICOLON
                  |              IDENTIFICADOR EQUALS expresion SUFIX tipo_dato SEMICOLON
    '''
    if len(t) == 5:    t[0] = Asignacion('local', Type.ANY, t[1], t[3], t.lineno(1), t.lexpos(0), None)
    elif len(t) == 6:  t[0] = Asignacion(t[1]   , Type.ANY, t[2], t[4], t.lineno(1), t.lexpos(0), None)
    elif len(t) == 7:  t[0] = Asignacion('local', t[5]    , t[1], t[3], t.lineno(1), t.lexpos(0), None)
        
# asignacion_struct
def p_asignacion_struct(t): # La que tiene SUFIX -> Es una declaracion, por lo que no requiere local ni global
    '''asignacion_struct : IDENTIFICADOR  PUNTO  IDENTIFICADOR EQUALS  expresion  SEMICOLON
    '''
#tipoVariable 
def p_tipoVariable(t):
    '''tipoVariable : GLOBAL 
                    | LOCAL
    '''
    t[0] = t[1]

# tipo_dato
def p_tipo_dato(t):
    '''tipo_dato : INT64 
                | FLOAT64 
                | BOOL 
                | CHAR 
                | STRING 
                | ARRAY 
                | NOTHING
                | IDENTIFICADOR  
    '''
    if   t[1] == 'Int64'  : t[0] = Type.INT
    elif t[1] == 'Float64': t[0] = Type.FLOAT
    elif t[1] == 'Bool'   : t[0] = Type.BOOL
    elif t[1] == 'Char'   : t[0] = Type.CHAR
    elif t[1] == 'String' : t[0] = Type.STRING
    elif t[1] == 'nothing': t[0] = Type.NULL
# callFunction
def p_callFunction(t):
    '''callFunction : callFunc SEMICOLON
    '''

def p_callFunc(t):
    '''callFunc : IDENTIFICADOR LPAR RPAR 
                | IDENTIFICADOR LPAR lista_expresion RPAR 
    '''
# sentencias
def p_sentencias(t):
    '''sentencias : lista_instrucciones
                  | 
    '''
# condicional
def p_condicional(t):
    '''condicional : IF  expresion  sentencias                                END SEMICOLON
                   | IF  expresion  sentencias               ELSE sentencias  END SEMICOLON
                   | IF  expresion  sentencias  elseifList                    END SEMICOLON
                   | IF  expresion  sentencias  elseifList   ELSE sentencias  END SEMICOLON 
    '''
# elseCond
def p_elseifList(t):
    '''elseifList : elseifList ELSEIF expresion sentencias
                  | ELSEIF expresion sentencias
    '''
# whileST 
def p_whileST(t):
    '''whileST : WHILE expresion sentencias END SEMICOLON
    '''
def p_forST(t):
    '''forST : FOR IDENTIFICADOR IN expresion sentencias END SEMICOLON
    '''
# lista_expresion
def p_lista_expresion(t):
    '''lista_expresion : lista_expresion COMMA expresion 
                       | expresion
    '''

#struct 
def p_struct(t):
    '''struct : MUTABLE STRUCT IDENTIFICADOR lista_atributos END SEMICOLON 
              |         STRUCT IDENTIFICADOR lista_atributos END SEMICOLON 
    '''

# lista_atributos
def p_lista_atributos(t):
    '''lista_atributos : lista_atributos IDENTIFICADOR SUFIX tipo_dato SEMICOLON
                       | lista_atributos IDENTIFICADOR                 SEMICOLON
                       |                 IDENTIFICADOR SUFIX tipo_dato SEMICOLON
                       |                 IDENTIFICADOR                 SEMICOLON
    '''

#inst_nativa
def p_inst_nativa(t):
    '''inst_nativa : PRINT      LPAR lista_expresion RPAR SEMICOLON
                   | PRINTLN    LPAR lista_expresion RPAR SEMICOLON
                   | PUSH       LPAR IDENTIFICADOR COMMA expresion RPAR SEMICOLON
                   | POP        LPAR IDENTIFICADOR COMMA expresion RPAR SEMICOLON
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
                 | expresion MOD expresion

                 | expresion DEQUALS expresion
                 | expresion DIFF expresion
                 | expresion GREATER expresion
                 | expresion LESSTHAN expresion
                 | expresion GEQ expresion
                 | expresion LEQ expresion

                 | IDENTIFICADOR
                 | IDENTIFICADOR  PUNTO  IDENTIFICADOR
                 | LPAR expresion RPAR
                 | primitivas
                 | nativas
                 | callFunc
                 | callArrays
    '''
    #print ((t.slice)) 
    if len(t) == 4: # SUM, DIV, MINUS
        if (t.slice[2].type =='SUM'):
            t[0] = Aritmeticas(t[1], Operador.PLUS, t[3], t.lineno(1), t.lexpos(0))    
            print (t[0].execute(None).value)
        elif (t.slice[2].type =='RESTA'):
            t[0] = Aritmeticas(t[1], Operador.MINUS, t[3], t.lineno(1), t.lexpos(0))
        elif (t.slice[2].type =='MUL'): 
            t[0] =  Aritmeticas(t[1], Operador.MUL, t[3], t.lineno(1), t.lexpos(0)) 
            print (t[0].execute(None).value)          
        elif (t.slice[2].type =='DIV'):
            t[0] = Aritmeticas(t[1], Operador.DIV, t[3], t.lineno(1), t.lexpos(0))           
        elif (t.slice[2].type =='POT'):
            t[0] = Aritmeticas(t[1], Operador.POT, t[3], t.lineno(1), t.lexpos(0))  
            print (t[0].execute(None).value)              
        elif (t.slice[2].type =='MOD'):
            t[0] = Aritmeticas(t[1], Operador.MOD, t[3], t.lineno(1), t.lexpos(0))            
            
    elif len(t) == 2: # primitivas, nativas, callFunc, callArrays, IDENTIFICADOR
        t[0] = t[1]
            
    
    
# callArrays 
def p_callArrays(t):
    '''callArrays : IDENTIFICADOR dimensiones
    '''
# dimensiones 
def p_dimensiones(t):
    '''dimensiones : dimensiones BRACKETA expresion BRACKETC
                   | BRACKETA expresion BRACKETC
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
   
    #print ("primitivas ->",t.slice)
    if (t.slice[1].type) == 'ENTERO':
        t[0] = Numerica(int(t[1]), Type.INT, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'DECIMAL':
        t[0] = Numerica( float(t[1]), Type.FLOAT, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'TRUE':
        t[0] = Primitivo(True, Type.BOOL, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'FALSE':
        t[0] = Primitivo(False, Type.BOOL, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'STRINGLITERAL':
        t[0] = Primitivo(str(t[1]).replace('"',''), Type.STRING, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'CHARLITERAL':
        t[0] = Primitivo(str(t[1]).replace("'",""), Type.CHAR, t.lineno(1), t.lexpos(0))
    elif t.slice[1].type == 'NOTHING':
        t[0] = Primitivo(None, Type.NULL, t.lineno(1), t.lexpos(0))
    elif len(t) == 3:
        t[0] = Primitivo([], Type.ARRAY, t.lineno(1), t.lexpos(0))
    else: 
        t[0] = Primitivo([], Type.ARRAY, t.lineno(1), t.lexpos(0))
        
# nativas
def p_nativas(t):
    '''nativas : SENO      LPAR expresion RPAR
               | COSENO    LPAR expresion RPAR
               | LOG       LPAR expresion COMMA expresion RPAR
               | LOG10     LPAR expresion RPAR
               | RAIZ      LPAR expresion RPAR
               | TANGENTE  LPAR expresion RPAR

               | LOWERCASE LPAR expresion RPAR  
               | UPPERCASE LPAR expresion RPAR
               | PARSE     LPAR tipo_dato COMMA expresion RPAR
               | TRUNC     LPAR tipo_dato COMMA expresion RPAR
               | FLOATCAST LPAR expresion RPAR
               | STRINGCAST LPAR expresion RPAR
               | TYPEOF    LPAR expresion RPAR         
    '''
    if len(t) == 5: # UPPERCASE, LOWERCASE, FLOATCAST, STRINGCAST, TYPEOF 
        if t.slice[1].type == 'UPPERCASE':
            t[0] = Uppercase(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'LOWERCASE':
            t[0] = Lowercase(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
    elif len(t) == 7:
        if t.slice[1].type == 'PARSE':
            t[0] = Parse(t[3], t[5], t.lineno(1), t.lexpos(0))
            print ("Valor traido del parse:", t[0].execute(None).value)
        elif t.slice[1].type == 'TRUNC':
            t[0] = Trunc(t[3], t[5], t.lineno(1), t.lexpos(0))
            print ("Valor traido del Trunc:", t[0].execute(None).value)
        

# items
def p_items(t):
    '''items : items COMMA expresion
             | expresion
    '''
def p_error(t):
    print("Syntax error in input!")
    print("Linea: ",t.lexer.lineno)
    print(t)
    


# Construyendo el analizador sintactico 

import ply.yacc as yacc 
parser = yacc.yacc()

file = open('./entrada.jl', 'r')
input = file.read()
#print(input)
parser.parse(input)

