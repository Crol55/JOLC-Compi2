from flask import Flask, render_template

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