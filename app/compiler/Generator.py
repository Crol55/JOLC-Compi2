

class Generator: 

    C3D_generator = None # Static variable -> Solo esta instancia existira 

    def __init__(self): # 
        # Contador para temporales y labels de C3D
        self.contadorVariablesTemporales = 0 
        self.contadorLabels = 0
        # Lugar donde se almacenara todo el codigo 3 direcciones
        self.codigo_C3D = ""
        self.codigo_funcionesNativas = "" # Almacenara el codigo C3D de las funciones nativas.
        # Lista de temporales 
        self.listaTemporales = []
        # banderas 
        self.inNativas = False
        self.inFuncion = False
        # Lista de funciones nativas ya implementadas
        self.listaNativas = { # Se inicializan en false para no duplicar el codigo
            'printString': False 
        }

    def addTemporal(self):
        temp = f"t{self.contadorVariablesTemporales}"
        self.contadorVariablesTemporales += 1
        self.listaTemporales.append( temp ) 
        return temp 

    def getInstance(self): # Aqui se crea o recupera la unica instancia existente de esta clase 'Generator'
        #print ("obteniendo instancia")
        if (Generator.C3D_generator == None): 
            Generator.C3D_generator = Generator() 
        return Generator.C3D_generator

    def insertCode(self, code, tab = "\t"): 

        if (self.inNativas):
            if (self.codigo_funcionesNativas == ''): 
                self.codigo_funcionesNativas = '/**** FUNCIONES NATIVAS *****/\n' # inicializarlo con un comentario

            self.codigo_funcionesNativas += tab + code 
        elif(self.inFuncion):
            pass
        else: # default -> inGlobalCode
            self.codigo_C3D += tab + code  
    

    def getHeader(self):
        header = "" 
        # Insertar cabecera de go 
        header += 'package main\n\n import (\n "fmt" \n)\n\n'
        if len(self.listaTemporales):
            header += "var "
            for indice in range( len(self.listaTemporales) ):
                header += self.listaTemporales[indice]
                if (indice < (len(self.listaTemporales)-1) ):
                    header += ","
            header += " float64;\n"
        header += "var stack[30102000] float64;\nvar heap[30102000] float64;\n"
        header += "var SP, H float64;\n"
        # concatenar el codigo 3 direcciones 
        header += "\n"+self.codigo_funcionesNativas + "\nfunc main(){\n" + self.codigo_C3D + "\n}"

        return header

    def add_newLine(self):
        self.insertCode("\n")

    def add_comment(self, comentario):
        self.insertCode(f'/*** {comentario} ***/\n')

    def add_if(self, left, right, op, label):
        self.insertCode(f'if({left} {op} {right}) {{goto {label};}}\n')
    
    def add_goto(self, label):
        self.insertCode( f'goto {label};\n' )


    def setFunctionHeader(self, functionName):
        self.insertCode("func "+functionName+ "(){\n", "")

    def setFuntionEnd(self):
        self.insertCode("return;\n}")

    ###################
    # LABELS
    ###################

    def add_label(self, label):
        self.insertCode(f'{label}:\n')
    
    def save_label(self, label):
        self.insertCode(f'{label}:\n')

    def generarLabel(self):
        newLabel = f"L{self.contadorLabels}"
        self.contadorLabels += 1
        return newLabel 
    
    ###################
    # FUNCIONES NATIVAS - println, println, len, casting, etc 
    # Las funciones nativas NO son definidas por el usuario sino definidas por nuestro lenguaje
    ###################

    def load_nativa_printString(self):
        # Verificar que no carguemos 2 veces la funcion nativa 
        function_name = "printString"
        already_loaded = self.listaNativas[function_name]

        if (not already_loaded):

            self.listaNativas[function_name] = True 
            self.inNativas = True # Para que el codigo se inserte en el string de nativas 

            # set inicio de funcion 
            self.setFunctionHeader(function_name)

            # codigo interno de la funcion nativa
            SP_index = self.addTemporal() 
            self.add_exp(SP_index, 'SP', '1', '+') # indice donde se encuentra el parametro 
            param1 = self.addTemporal() 
            self.getFromStack(param1, SP_index) # sabemos que el valor que tendra param1, hace referencia a una posicion del heap

            # while para iterar el heap 
            init = self.generarLabel()
            fin  = self.generarLabel() 
            self.save_label(init) 

            # char value =  
            char_temp = self.addTemporal()
            self.getFromHeap(char_temp, param1)

            # verificar si no es fin de cadena 
            self.add_if(char_temp, '-1', '==', fin)

            # si no es fin de cadena, imprimir e incrementar el iterador 
            self.add_print('c', char_temp) 
            self.add_exp(param1, param1, '1', '+')

            self.add_goto(init)
            self.save_label(fin)

            # set fin de funcion
            self.setFuntionEnd() 
            self.inNativas = False
            # Insertar la cabecera de la funcion


    ###################
    # STACK
    ###################
    def putIntoStack(self, pos, value ):
        self.insertCode( f'stack[int({pos})] = {value};\n' )

    def getFromStack(self, temporal:str, pos):
        self.insertCode(f'{temporal}=stack[int({pos})];\n')

    ###################
    # HEAP
    ###################
    def putIntoHeap(self, index, value):  
        self.insertCode(f'heap[int({index})] = {value};\n')

    def increaseHeapPointer(self):
        self.insertCode(f'H = H+1;\n')   

    def getFromHeap(self, temporal: str, index):
        self.insertCode(f'{temporal}=heap[int({index})];\n')

    ###################
    # EXPRESIONES
    ###################
    def add_exp(self, temp:str, leftVal:str, rightVal:str, operador:str, comentario = ""):

        if comentario != "": 
            comentario = f'/*{comentario}*/'

        instruccion = f"{temp} = {leftVal} {operador} {rightVal}; {comentario}\n"
        self.insertCode(instruccion)
    ###################
    # Manejo de Ambitos y funciones
    ###################

    def newAmbito(self, size):
        moveStackPointer = f"SP = SP + {size};\n"
        self.insertCode(moveStackPointer)
    
    def returnAmbito(self, size): 
        restoreStackPointer = f"SP = SP - {size};\n"
        self.insertCode(restoreStackPointer)

    def callFunction(self, nombreFuncion):
        self.insertCode(f'{nombreFuncion}();\n')
    
    ###################
    # INSTRUCCIONES 
    ###################

    def add_print(self, type, value, cast="int"): # Impresion nativa de GOlang 
        instruccion = f'fmt.Printf("%{type}", {cast}({value}) );'
        self.insertCode(instruccion)
        self.add_newLine()

    def add_print_true(self ):
        self.add_print("c", 116)
        self.add_print("c", 114)
        self.add_print("c", 117)
        self.add_print("c", 101)

    def add_print_false(self ):
        self.add_print("c", 102)
        self.add_print("c", 97)
        self.add_print("c", 108)
        self.add_print("c", 115)
        self.add_print("c", 101)
    