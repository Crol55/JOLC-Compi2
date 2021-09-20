

from Instrucciones.AsignacionArray import AsignacionArray
from Expresiones.AccesoArrays import AccesoArrays
from Expresiones.nativas.Length import Length
from Instrucciones.nativas.Pop import Pop
from Instrucciones.nativas.Push import Push
from Primitivas.Array import Array
from Expresiones.Range import Range
from Instrucciones.Loops.For import For
from Instrucciones.Structs.AsignacionStruct import AsignacionStruct
from Instrucciones.Structs.AccesoStruct import AccesoStruct
from Instrucciones.Structs.CrearStruct import CrearStruct
from Instrucciones.Loops.While import While
from Instrucciones.Condicional.Sentencia import Sentencia
from Instrucciones.Condicional.If import If
from Instrucciones.nativas.Print import Print
from Instrucciones.Functions.CallFunction import CallFunction
from Instrucciones.Transferencia.Break import Break
from Instrucciones.Transferencia.Continue import Continue
from Instrucciones.Transferencia.ReturnINST import ReturnINST
from Instrucciones.Functions.Parametro import Parametro
from Instrucciones.Functions.Funcion import Funcion
from Expresiones.Acceso import Acceso
from Operaciones.Logicas import Logicas, OperadorLogico, Not
from Operaciones.Relacional import OperadorRelacional, Relacional
from Expresiones.nativas.LogaritmoBaseDiez import LogaritmoBaseDiez
from Expresiones.nativas.Logaritmo import Logaritmo
from Expresiones.nativas.Raiz import Raiz
from Expresiones.Trigonometricas import Trigonometricas
from Nativas.Type import Type
from Primitivas.Numerica import Numerica
from Primitivas.Primitivo import Primitivo
from Operaciones.Aritmeticas import Aritmeticas,Operador
from Instrucciones.Asignacion import Asignacion
from Expresiones.Nativas import *
from Expresiones.Parse   import *
from Expresiones.Trunc   import *
from Expresiones.Floatcast import Floatcast
from Expresiones.Stringcast import Stringcast
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
    'length' : 'LENGTH'
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
    'PUNTO',
    'DOSPUNTOS'
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
t_DOSPUNTOS = r':'
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
    t.lexer.lineno += t.value.count("\n")   

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
     print("Error lexico, Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

# Construir el analizador lexico 
import ply.lex as lex 
lexer = lex.lex()

'''
    ===================== ANALISIS SINTACTICO ============================ 
'''

precedence = (
    
    ('left', 'DOSPUNTOS'),
    ('left', 'AND', 'OR'),
    ('left', 'GREATER','LESSTHAN', 'GEQ', 'LEQ'),
    ('left', 'DEQUALS', 'DIFF'),
    ('left', 'SUM', 'RESTA'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('right', 'POT'),
    ('right', 'UMINUS')
 )
# Definicion de producciones 
def p_inicio(t): 
    'inicio : instrucciones'

    #print("Cantidad de instrucciones: ", (t[1]))
    #for ins in t[1]: 
    #    print(ins.execute(None))
    t[0] = t[1]

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
        t[0] = t[1]
    else: 
        t[0] = t[1] 

# declareFunction -> | FUNCTION IDENTIFICADOR LPAR                  RPAR lista_instrucciones   SEMICOLON

def p_declareFunction(t):
    '''declareFunction : FUNCTION IDENTIFICADOR LPAR                  RPAR                      END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR lista_instrucciones  END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR                  RPAR lista_instrucciones  END SEMICOLON
                       | FUNCTION IDENTIFICADOR LPAR lista_parametros RPAR                      END SEMICOLON
    '''
    # 9 , 7 , 8, 
    if len(t) == 7:
        t[0] = Funcion(t[2], [], [], t.lineno(1), t.lexpos(0), None) # Produccion 1
    elif len(t) == 8:
        if (t.slice[4].type == 'lista_parametros'):
            t[0] = Funcion(t[2],t[4],[], t.lineno(1), t.lexpos(0), None) # produccion 4
        else: 
            t[0] = Funcion(t[2],[],t[5], t.lineno(1), t.lexpos(0), None) # produccion 3
    else:
        t[0] = Funcion(t[2],t[4],t[6], t.lineno(1), t.lexpos(0), None) # produccion 2
        #print ("Ingreso con la ultima funcion",t[2], t[6])

# lista_instrucciones
def p_lista_instrucciones(t):
    '''lista_instrucciones : lista_instrucciones instruccion
                           | lista_instrucciones transferencia
                           | instruccion
                           | transferencia
    '''
    if len(t) == 2: # instruccion o transferencia, pero a esta especificamente solo ingresa 1 vez
        t[0] = [ t[1] ]
    else:
        t[1].append( t[2] )
        t[0] = t[1]
        
    
# transferencia
def p_transferencia(t):
    '''transferencia : BREAK SEMICOLON
                     | CONTINUE SEMICOLON
                     | returnValue SEMICOLON
    '''
    tipo_transferencia = t.slice[1].type 
    if tipo_transferencia == 'BREAK': 
        t[0] = Break(t.lineno(1), t.lexpos(0), None)
    elif tipo_transferencia == 'CONTINUE': 
        t[0] = Continue(t.lineno(1), t.lexpos(0), None)
    else: # Produccion 3
        t[0] = t[1]

# returnValue
def p_returnValue(t):
    '''returnValue : RETURN expresion 
                   | RETURN 
    '''
    if len(t) == 3: # Produccion 1  
        t[0] = ReturnINST(t[2], t.lineno(1), t.lexpos(0), None)
    else: # Produccion 2
        t[0] = ReturnINST(None, t.lineno(1), t.lexpos(0), None)

# lista_parametros
def p_lista_parametros(t):
    '''lista_parametros : lista_parametros COMMA IDENTIFICADOR 
                        | lista_parametros COMMA IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR SUFIX tipo_dato
                        | IDENTIFICADOR
    ''' 
    if len(t) == 2: 
        t[0] = [Parametro(t[1], Type.ANY, t.lineno(1), t.lexpos(0), None)] # Produccion 4
    elif len(t) == 4: 
        if t.slice[1].type == 'lista_parametros':  # Produccion 1
            t[1].append( Parametro(t[3], Type.ANY, t.lineno(1), t.lexpos(0), None) )
            t[0] = t[1]
        else: # Produccion 3 
           t[0] = [Parametro(t[1], t[3], t.lineno(1), t.lexpos(0), None)] 

    elif len(t) == 6: # Produccion 2
        t[1].append( Parametro(t[3], t[5], t.lineno(1), t.lexpos(0), None) )
        t[0] = t[1]
        

# Asignacion        
def p_asignacion(t): # La que tiene SUFIX -> Es una declaracion, por lo que no requiere local ni global
    '''asignacion :              IDENTIFICADOR EQUALS expresion                 SEMICOLON
                  |              IDENTIFICADOR EQUALS expresion SUFIX tipo_dato SEMICOLON
                  | tipoVariable IDENTIFICADOR EQUALS expresion                 SEMICOLON
                  | tipoVariable IDENTIFICADOR EQUALS expresion SUFIX tipo_dato SEMICOLON
                  | IDENTIFICADOR dimensiones EQUALS expresion SEMICOLON
    '''
    if len(t) == 5:    t[0] = Asignacion('', Type.ANY, t[1], t[3], t.lineno(1), t.lexpos(0), None) # Prod -> 1
    elif len(t) == 6:
        if t.slice[1].type == 'tipoVariable':  # prod -> 3
            t[0] = Asignacion(t[1]   , Type.ANY, t[2], t[4], t.lineno(1), t.lexpos(0), None)
        else: # prod -> 5
            t[0] = AsignacionArray(t[1], t[2], t[4], Type.ANY,t.lineno(1), t.lexpos(0), None)
    elif len(t) == 7:  t[0] = Asignacion('', t[5]    , t[1], t[3], t.lineno(1), t.lexpos(0), None)
    elif len(t) == 8:  t[0] = Asignacion(t[1],    t[6]    , t[2], t[4], t.lineno(1), t.lexpos(0), None)
        
# asignacion_struct
def p_asignacion_struct(t): # La que tiene SUFIX -> Es una declaracion, por lo que no requiere local ni global
    '''asignacion_struct : IDENTIFICADOR  PUNTO  IDENTIFICADOR EQUALS  expresion  SEMICOLON
    '''
    t[0] = AsignacionStruct(t[1], t[3], t[5], t.lineno(1), t.lexpos(0))
    
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
    #print("Que carajo hay aqui?", t[1])
    if   t[1] == 'Int64'  : t[0] = Type.INT
    elif t[1] == 'Float64': t[0] = Type.FLOAT
    elif t[1] == 'Bool'   : t[0] = Type.BOOL
    elif t[1] == 'Char'   : t[0] = Type.CHAR
    elif t[1] == 'String' : t[0] = Type.STRING
    elif t[1] == 'nothing': t[0] = Type.NULL
    else: t[0] = t[1]
     
# callFunction
def p_callFunction(t):
    '''callFunction : callFunc SEMICOLON
    '''
    t[0] = t[1]

def p_callFunc(t): # Puede llamar a una Funcion o llamar a un struct, ya que se declaran de la misma forma
    '''callFunc : IDENTIFICADOR LPAR RPAR 
                | IDENTIFICADOR LPAR lista_expresion RPAR 
    '''
    if len(t) == 4: # produccion 1
        t[0] = CallFunction(t[1], [], t.lineno(1), t.lexpos(0), None)  
    else: # Produccion 2
        t[0] = CallFunction(t[1], t[3], t.lineno(1), t.lexpos(0), None) 

# sentencias
def p_sentencias(t):
    '''sentencias : lista_instrucciones
                  | 
    '''
    if len (t) == 2: # produccion 1
        t[0] = Sentencia(t[1], t.lineno(1), t.lexpos(0), None) 
    else:  # produccion 2
        t[0] = None #Empty array  

# condicional
def p_condicional(t):
    '''condicional : IF  expresion  sentencias                                END SEMICOLON
                   | IF  expresion  sentencias  elseifList                    END SEMICOLON
                   | IF  expresion  sentencias               ELSE sentencias  END SEMICOLON
                   | IF  expresion  sentencias  elseifList   ELSE sentencias  END SEMICOLON 
    '''
    
    if len(t) == 6: #produccion 1 
        t[0] = If(t[2], t[3], None, t.lineno(1), t.lexpos(0), None) 
    elif len (t) == 7: #produccion 2
        t[0] = If(t[2], t[3], t[4], t.lineno(1), t.lexpos(0), None) 
    elif len (t) == 8: #produccion 3
        print ("El usuario quiere ejecutar un If sin de produccion #3")
        t[0] = If(t[2], t[3], t[5], t.lineno(1), t.lexpos(0), None) 
    elif len (t) == 9: #produccion 4
        print ("El usuario quiere ejecutar la produccion 4")

        elseif_list = t[4]

        while True: # Iterar hasta que se encuentre None para poder insertar alli el ELSE
            if elseif_list.else_or_elseif == None: 
                elseif_list.else_or_elseif = t[6]
                break
            elseif_list = elseif_list.else_or_elseif
        
        t[0] = If(t[2], t[3], t[4], t.lineno(1), t.lexpos(0), None) 

# elseCond
def p_elseifList(t):
    '''elseifList : elseifList ELSEIF expresion sentencias
                  | ELSEIF expresion sentencias
    '''
    if len(t) == 5: # produccion 1 
        
        newElseif = If(t[3], t[4], None, t.lineno(1), t.lexpos(0), None)
        previous_if = t[1]

        while True: # Iterar hasta que se encuentre None para poder insertarlo alli
            if previous_if.else_or_elseif == None: 
                previous_if.else_or_elseif = newElseif
                break
            previous_if = previous_if.else_or_elseif
        t[0] = t[1]
                
    else: # produccion 2
        t[0] = If(t[2], t[3], None, t.lineno(1), t.lexpos(0), None) # El primer elseif de la produccion



# WHILE 
def p_whileST(t):
    'whileST : WHILE expresion sentencias END SEMICOLON'
    t[0] = While(t[2], t[3], t.lineno(1), t.lexpos(0), None)


# FOR 
def p_forST(t):
    'forST : FOR IDENTIFICADOR IN expresion sentencias END SEMICOLON'
    t[0] = For(t[2], t[4], t[5], t.lineno(1), t.lexpos(0))


# lista_expresion
def p_lista_expresion(t):
    '''lista_expresion : lista_expresion COMMA expresion 
                       | expresion
    '''
    if len (t) == 2:  # produccion 2
        t[0] = [ t[1] ]
    else:  # produccion 1
        t[1].append( t[3] )
        t[0] = t[1]


#struct 
def p_struct(t):
    '''struct : MUTABLE STRUCT IDENTIFICADOR lista_atributos END SEMICOLON 
              |         STRUCT IDENTIFICADOR lista_atributos END SEMICOLON 
    '''
    #print ("El user va a crear un struct")
    if len(t) == 7: # produccion 1
        t[0] = CrearStruct(True, t[3], t[4], t.lineno(2), t.lexpos(0), None) 
    else: # produccion 2 
        t[0] = CrearStruct(False, t[2], t[3], t.lineno(1), t.lexpos(0), None)

# lista_atributos
def p_lista_atributos(t):
    '''lista_atributos : lista_atributos IDENTIFICADOR SUFIX tipo_dato SEMICOLON
                       | lista_atributos IDENTIFICADOR                 SEMICOLON
                       |                 IDENTIFICADOR SUFIX tipo_dato SEMICOLON
                       |                 IDENTIFICADOR                 SEMICOLON
    '''
    #print (t.slice)
    if len(t) == 6: #produccion 1 
        #print("Ingreso a la produccion 3->",t[2], t[4])
        t[1].append( Parametro(t[2], t[4], t.lineno(2), t.lexpos(0), None) )
        t[0] = t[1] 
    elif len(t) == 4: #produccion 2 
        t[1].append( Parametro(t[2], Type.ANY, t.lineno(2), t.lexpos(0), None) )
        t[0] = t[1]
    elif len(t) == 5 : #produccion 3 
        
        t[0] =  [ Parametro(t[1],     t[3], t.lineno(2), t.lexpos(0), None) ]  
    elif len(t) == 3: #produccion 4
        t[0] =  [ Parametro(t[1], Type.ANY, t.lineno(2), t.lexpos(0), None) ] 
    

#inst_nativa
def p_inst_nativa(t):
    '''inst_nativa : PRINT      LPAR lista_expresion RPAR SEMICOLON
                   | PRINTLN    LPAR lista_expresion RPAR SEMICOLON
                   | PUSH       LPAR IDENTIFICADOR COMMA expresion RPAR SEMICOLON
                   | POP        LPAR IDENTIFICADOR                 RPAR SEMICOLON
    '''
    if t.slice[1].type == 'PRINT':
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0), None, False)
    if t.slice[1].type == 'PRINTLN':
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0), None, True)
    if t.slice[1].type == 'PUSH':
        t[0] = Push(t[3],t[5], t.lineno(1), t.lexpos(0), None)
    if t.slice[1].type == 'POP':
        t[0] = Pop(t[3], t.lineno(1), t.lexpos(0), None)

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

                 | expresion DOSPUNTOS expresion

                 | IDENTIFICADOR
                 | IDENTIFICADOR  operador_punto
                 | LPAR expresion RPAR
                 | primitivas
                 | nativas
                 | callFunc
                 | callArrays
    '''
    #print ((t.slice)) 
    if len(t) == 3:  # NOT, 
        if t.slice[1].type == 'NOT': 
            t[0] = Not( t[2], t.lineno(1), t.lexpos(0))
            
        elif t.slice[1].type == 'RESTA': # Uminus
            t[0] = Aritmeticas(Numerica(0, Type.INT,t.lineno(1), t.lexpos(0)), Operador.MINUS, t[2], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif (t.slice[1].type =='IDENTIFICADOR'): # | IDENTIFICADOR  operador_punto
            #print ("Quiere acceder a una variable del struct !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            t[0] = AccesoStruct(t[1], t[2][0], t.lineno(1), t.lexpos(0), None)

    elif len(t) == 4: # SUM, DIV, MINUS
        if (t.slice[2].type =='SUM'): t[0] = Aritmeticas(t[1], Operador.PLUS, t[3], t.lineno(2), t.lexpos(2))    
            #print (t[0].execute(None).value)
        elif (t.slice[2].type =='RESTA'):
            t[0] = Aritmeticas(t[1], Operador.MINUS, t[3], t.lineno(2), t.lexpos(0))
        elif (t.slice[2].type =='MUL'): 
            #print ("El mul se ejecuta antessssssssssssssssssssssssssssssssssssssssssssssss",t.lineno(2))
            t[0] =  Aritmeticas(t[1], Operador.MUL, t[3], t.lineno(2), t.lexpos(0)) 
            #print (t[0].execute(None).value)          
        elif (t.slice[2].type =='DIV'):
            t[0] = Aritmeticas(t[1], Operador.DIV, t[3], t.lineno(2), t.lexpos(0))           
        elif (t.slice[2].type =='POT'):
            t[0] = Aritmeticas(t[1], Operador.POT, t[3], t.lineno(2), t.lexpos(0))  
            #print (t[0].execute(None).value)              
        elif (t.slice[2].type =='MOD'):
            t[0] = Aritmeticas(t[1], Operador.MOD, t[3], t.lineno(2), t.lexpos(0))
        elif (t.slice[2].type =='DEQUALS'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.DEQUAL, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)
        elif (t.slice[2].type =='DIFF'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.DISTINT, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)
        elif (t.slice[2].type =='GREATER'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.GREATER, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)    
        elif (t.slice[2].type =='LESSTHAN'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.LESS, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)   
        elif (t.slice[2].type =='GEQ'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.GEQ, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)   
        elif (t.slice[2].type =='LEQ'):
            t[0] = Relacional(t[1], t[3], OperadorRelacional.LEQ, t.lineno(2), t.lexpos(2))  
            #print (t[0].execute(None).value)  
        elif (t.slice[2].type =='AND'):
            t[0] = Logicas(t[1], t[3], OperadorLogico.AND, t.lineno(2), t.lexpos(2))
            #print (t[0].execute(None).value)   
        elif (t.slice[2].type =='OR'):
            t[0] = Logicas(t[1], t[3], OperadorLogico.OR, t.lineno(2), t.lexpos(2))
            
        elif (t.slice[2].type =='DOSPUNTOS'): #expresion DOSPUNTOS expresion
            t[0] = Range(t[1],t[3], t.lineno(2), t.lexpos(2))

        elif (t.slice[1].type == 'LPAR'): 
            t[0] = t[2]
            
    elif len(t) == 2: # primitivas, nativas, callFunc, callArrays, IDENTIFICADOR
        if t.slice[1].type == 'IDENTIFICADOR':
            t[0] = Acceso(str(t[1]), t.lineno(1), t.lexpos(0)) 
        else: 
            t[0] = t[1]
            

# Operador_punto 
def p_operador_punto(t):
    '''operador_punto : operador_punto PUNTO  IDENTIFICADOR
                      | PUNTO  IDENTIFICADOR
    ''' 
    if len(t) == 4: 
        t[1].append( t[3] )
        t[0] = t[1]  
    else: 
        t[0] = [ t[2] ] # arreglo de indentificadores    
    
# callArrays 
def p_callArrays(t):
    '''callArrays : IDENTIFICADOR dimensiones
    '''
    t[0] = AccesoArrays(t[1], t[2], t.lineno(1), t.lexpos(0), None)
# dimensiones 
def p_dimensiones(t):
    '''dimensiones : dimensiones BRACKETA expresion BRACKETC
                   | BRACKETA expresion BRACKETC
    '''
    if len(t) == 5: 
        t[1].append(  t[3]  ) 
        t[0] = t[1]
    else: 
        t[0] = [ t[2] ] # creamos el arreglo de expresiones


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
        t[0] = Array([], t.lineno(1), t.lexpos(0)) #   | BRACKETA BRACKETC
    else: 
        t[0] = Array(t[2], t.lineno(1), t.lexpos(0)) # | BRACKETA items BRACKETC
        
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
               | LENGTH    LPAR expresion RPAR
    '''
    if len(t) == 5: # UPPERCASE, LOWERCASE, FLOATCAST, STRINGCAST, TYPEOF 
        if t.slice[1].type == 'UPPERCASE':
            t[0] = Uppercase(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'LOWERCASE':
            t[0] = Lowercase(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'FLOATCAST':
            t[0] = Floatcast(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'STRINGCAST':
            t[0] = Stringcast(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'TYPEOF':
            t[0] = typeof(t[3], t.lineno(1), t.lexpos(0))
            #print (t[0].execute(None).value)
        elif t.slice[1].type == 'SENO': 
            t[0] = Trigonometricas(t[3], t[1], t.lineno(1), t.lexpos(0))       
        elif t.slice[1].type == 'COSENO': 
            t[0] = Trigonometricas(t[3], t[1], t.lineno(1), t.lexpos(0)) 
        elif t.slice[1].type == 'TANGENTE': 
            t[0] = Trigonometricas(t[3], t[1], t.lineno(1), t.lexpos(0))
        elif t.slice[1].type == 'LOG10': 
            t[0] = LogaritmoBaseDiez(t[3], t.lineno(1), t.lexpos(0)) 
        elif t.slice[1].type == 'RAIZ': 
            t[0] = Raiz(t[3], t.lineno(1), t.lexpos(0)) 
        elif t.slice[1].type == 'LENGTH': 
            t[0] = Length(t[3], t.lineno(1), t.lexpos(0), None)
            
    elif len(t) == 7:
        if t.slice[1].type == 'PARSE':
            t[0] = Parse(t[3], t[5], t.lineno(1), t.lexpos(0))
            #print ("Valor traido del parse:", t[0].execute(None).value)
        elif t.slice[1].type == 'TRUNC':
            t[0] = Trunc(t[3], t[5], t.lineno(1), t.lexpos(0))
            #print ("Valor traido del Trunc:", t[0].execute(None).value)
        elif t.slice[1].type == 'LOG': 
            t[0] = Logaritmo(t[3],t[5], t.lineno(1), t.lexpos(0)) 
            #print(t[0].execute(None).value) 
        

# items
def p_items(t):
    '''items : items COMMA expresion
             | expresion
    '''
    if len(t) == 4: # produccion 1
        t[1].append( t[3] )
        t[0] = t[1]
    else: # produccion 2
        t[0] = [ t[1] ] 
    
# Error
def p_error(t):
    print("Error sintactico en la entrada!")
    print("Linea: ",t.lexer.lineno)
    print(t)
    


# Construyendo el analizador sintactico 

import ply.yacc as yacc 
parser = yacc.yacc()


def interpretar(input): 
    #print(input)
    return parser.parse(input)

