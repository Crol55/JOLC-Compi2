from flask import Flask, render_template, request
#from .gramatica import interpretar
#from .Tabla_Simbolos.Ambito import Ambito
#from .Nativas.Type import Type

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
    
    

    return { "msg": "todo correcto", "code": 200}

if __name__ == "__main__":
    app.run()
    #app.run( debug=True, port=4000)