
mutable struct circulo 
    color;
    colorcito::bool; 
end; 


struct circulo2 
    color;
    colorcito::bool; 
end; 



#function testeo(val)
#    struct test
#        t;
#    end;
#    println("hola mundo");
#    circulo();
#    # neceisto utilizarla ahora... xD
#end;
#
#testeo(10);


# multiplicar 2 numeros sin usar la multiplicacion

function sum(val1, val2) 

    #println("conteo:", val1); 
    val1 = val1 + 1;
    #println("Luego de incrementar:", val1);
    if val1 > val2
        println("Aqui solo deberia ingresar una vez================", val1, " ", val2);
        return 20; #hubieron 2 return seguidos.. cuidado
    else 
        #println("Con que valor va a llamar a otra funcion ==============>", val1);
        res = sum(val1, val2);
        println("Que valor tendra aqui", res);
        println("Aqui deberia ser 1 menos creo:", val1);
    end;

end;
val = 0;
println("El verdade",sum(2, 5));

function f1 ()

    if true 
        println("PORQUE ENTRA DOS VECES AQUI =================================================");
        return 10;
    end; 
    
end; 


function f2() 
    println("Este mensaje fijo funciona");
    f1(); 
    #println("Este ya no va a funcionar",f1());
end; 

#println(f2());
# println("Que putas mano?:",sum(2, 10)); esta sentencia no esta funcionando, las funciones no estan retornando nada
