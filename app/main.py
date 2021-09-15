from flask import Flask, render_template, request
#from gramatica import interpretar
from Tabla_Simbolos.Ambito import Ambito
from Nativas.Type import Type
from Export import Output



app = Flask(__name__)

@app.route("/")
def root_view():
    return render_template('index.html')

@app.route('/home')
def home_view(): 
    return render_template('home.html')

@app.route('/analisis')
def analisis_view(): 
    return render_template('analisis.html')


@app.route('/analizar', methods=['POST'])
def analizar():
    
    code = request.json['input']
    print("Me estoy ejecutando chato", code)

    #newAmbitoGlobal = Ambito(None) # Este funciona como el ambito GLOBAL
    #ast = interpretar(code)
#
    #print (" ================ EXECUTING FROM MAIN.PY ============================")
    #Output.init() # Inicializamos nuestras variables globales, estas luego de ejecutar el interprete, se retornaran al frontend
    ##try : 
    #for instruccion in ast: 
    #    retMain = instruccion.execute(newAmbitoGlobal)
    #    if retMain != None: # Podria ser un (return, break, o continue) y eso no se permite a menos que este en un loop
    #        if type(retMain) == bool: 
    #            print ("Main.py: Una instruccion esta retornando algo distinto a None")
    #            if retMain == False: # Hubo un error con alguna instruccion 
    #                print("Main.py: Error en una instruccion: el interprete detuvo la ejecucion")
    #                break
    #        elif retMain.type == Type.BREAK: 
    #            print("Error sintactico: Un 'break' no puede ser declarado afuera de un loop.")
    #            break
    #        elif retMain.type == Type.CONTINUE: 
    #            print("Error sintactico: Un 'continue' no puede ser declarado afuera de un loop.")
    #            break
    ##except: 
    # #   print("Error Fatal al ejecutar instrucciones")
#
#
    #return { "estado": True, "msg": Output.salidaInterprete, "code": 200}



if __name__ == "__main__":
    app.run()
    #app.run( debug=True, port=4000)