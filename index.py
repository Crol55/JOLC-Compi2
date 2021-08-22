
from flask import Flask

app = Flask(__name__)

@app.route('/')
def raiz():
    return "Hola mundo desde python, pero esto tambien debe funcionar"

# print (__name__)
if (__name__ == '__main__'):
    app.run( debug=True, port=4000)
