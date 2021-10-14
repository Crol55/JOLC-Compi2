

class Generator: 

    C3D_generator = None # Static variable -> Solo esta instancia existira 

    def __init__(self): # 
        # Contador para temporales y labels de C3D
        self.contadorVariablesTemporales = 0 
        self.contadorLabels = 0
        # Lugar donde se almacenara todo el codigo 3 direcciones
        self.codigo_C3D = ""
        # Lista de temporales 
        self.listaTemporales = []
        # banderas 
        self.inNativas = False
        self.inFuncion = False

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
            pass
        elif(self.inFuncion):
            pass
        else: # default -> inGlobalCode
            self.codigo_C3D += tab + code  

    def getHeader(self):
        header = "" 
        # Insertar cabecera de go 
        header += 'package main\n\n import (\n "fmt" \n)\n\n'
        header += "var "
        for indice in range( len(self.listaTemporales) ):
            header += self.listaTemporales[indice]
            if (indice < (len(self.listaTemporales)-1) ):
                header += ","
        header += " float64\n"
        # concatenar el codigo 3 direcciones 
        header += "\nfunc main(){\n" + self.codigo_C3D + "\n}"

        return header

    def add_newLine(self):
        self.insertCode("\n")



    ###################
    # EXPRESIONES
    ###################
    def add_exp(self, temp, leftVal, rightVal, operador):

        instruccion = f"{temp} = {leftVal} {operador} {rightVal}; \n"
        self.insertCode(instruccion)
    
    ###################
    # INSTRUCCIONES (print), (println)
    ###################

    def add_print(self, type, value, cast="int"): # Impresion nativa de GOlang 
        instruccion = f'fmt.Printf("%{type}", {cast}({value}) )'
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
    