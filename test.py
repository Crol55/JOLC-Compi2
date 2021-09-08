

#import math 
#print (type (5))
#print (math.sin(6))
#print (math.log10(5))
#print (math.log(5,10))
#print (math.sqrt(25))
#
#arr = {}
#if 'x' in arr.keys(): 
#    print("Si jala tecero?")
#else: print("nuay")

def sum(val1, val2):

    print("conteo:", val1) 
    val1 = val1 + 1
    print("Luego de incrementar:", val1)
    if val1 > val2:
        print("Aqui solo deberia ingresar una vez") 
        return 20; #hubieron 2 return seguidos.. cuidado
    else: 
        sum(val1, val2)
        print("Aqui deberia ser 1 menos creo:", val1)
    


sum(2, 5)



