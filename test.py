
from Primitivas.Numerica import *
from Operaciones.Aritmeticas import Aritmeticas, Operador
from Nativas.Type import Type
import re
val1 = Numerica(10, Type.INT, 10,15)
val2 = Numerica(10.6, Type.FLOAT, 10,15)
val3 = Numerica(30, Type.INT, 10,15)

arreglo = [val1, val2, val3]

#for vals in arreglo:
 #   print (vals.execute(None))

operacion = Aritmeticas(val1, Operador.PLUS, val2,1,1) #Aritmeticas(val1, '+', val2,1,1)
#print (operacion.execute(None).value)

operacion.execute(None)

print ("hola" * 3)

print (float("-10.23"))
