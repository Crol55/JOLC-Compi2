from flask import Flask, render_template, request
from gramatica import interpretar
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type import Type
from Export import Output
import sys 
# Agregado en proyecto #2
from compiler.Generator import Generator

app = Flask(__name__)

@app.route("/")
def root_view():
    return render_template('home.html')

@app.route('/home')
def home_view(): 
    return render_template('home.html')

@app.route('/analisis')
def analisis_view(): 
    return render_template('analisis.html')


@app.route('/compilar_codigo', methods=['POST'])
def compilar_codigo(): 

    juliaCode = request.json['input'] 

    ast = interpretar(juliaCode)

    # area de compilador 
    newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
    Generator.C3D_generator = None # Limpiamos para que no se concatenen las instrucciones

    for instruccion in ast: # Aqui se vuelve a generar -> Generator.C3D_generator
        instruccion.compile(newAmbitoGlobal)

    static_gen = Generator.C3D_generator 
    if (static_gen): 
        c3d_code = static_gen.getHeader()
        print(" =================== Codigo 3 direcciones ===================")
        print( c3d_code)
        print ("=================== Fin Codigo 3 direcciones ===================")
        return {"msg": c3d_code}
    return {"msg": "Error"}


@app.route('/analizar', methods=['POST'])
def analizar():
    
    code = request.json['input']
    print("Me estoy ejecutando chato", code)

    sys.setrecursionlimit(2500)
    newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
    ast = interpretar(code)

    print (" ================ EXECUTING FROM MAIN.PY ============================")
    Output.init() # Inicializamos nuestras variables globales, estas luego de ejecutar el interprete, se retornaran al frontend
    #try : 
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
    #except: 
     #   print("Error Fatal al ejecutar instrucciones")


    return { "estado": True, "msg": Output.salidaInterprete, "code": 200}


@app.route('/reportes')
def reportes_view():
    return render_template('reportes.html', cond = True)


@app.route('/get_specific_report', methods=['POST'])
def get_report():
    tipo_reporte =  request.json['tipo']#request.query_string['tipo']#request.args['tipo']
    print ("Que tipo de reporte enviaron", tipo_reporte)
    if tipo_reporte == 'errores': 
        try: 
            lista_errores  = Output.errorSintactico
            newLista = [] 
            for err in lista_errores: 
                print (err.descripcion) 
                newLista.append( {"descripcion": err.descripcion, "linea":err.linea, "columna": err.columna, "time": err.time})
            
            return { "estado": True, "msg": newLista, "code": 200} 
        except:
            return { "estado": False, "msg": "No existen errores", "code": 200}

    elif tipo_reporte == 'simbolos': 
        try: 
            lista = Output.tablaSimbolos
            return { "estado": True, "msg": lista, "code": 200} 
        except:
            return { "estado": False, "msg": "Debe analizar su codigo de JOLC para que exista una tabla de simbolos", "code": 200}
    elif tipo_reporte == 'CST': 
        try: 
            CST = Output.AST
            return { "estado": True, "msg": CST, "code": 200} 
        except:
            return { "estado": False, "msg": "Debe analizar su codigo de JOLC para que exista un arbol de analisis sintactico", "code": 200} 
    return {"estado": "siu"}


if __name__ == "__main__":
    #app.run()
    app.run( debug=True, port=4000)