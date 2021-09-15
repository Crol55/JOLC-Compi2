
#=mutable struct circulo 
    color;
    colorcito::Bool; 
end; 


#struct circulo2 
#    color;
#    colorcitosss::Bool; 
#end; 

circ = circulo("azul", true);
#val = circ.colorcito;
#test = 10;
circ.colorcito = "black";
#print ("El val es:", typeof(circ));
println("El valor debe ser 20:", circ.colorcito);
=# 
#for val in "hola mundo!" 
#    print(val, "-");
#    if val == "m"
#        return 20;
#    end; 
#    println ("NO DEBIO");
#end;
valores = float(1300);
println("Quiay:", typeof(valores));
mayuscula = uppercase("HOLa");
println(mayuscula);
println(lowercase("MUNDO"));
println( parse(Int64, "20.3") );
x = tan(3);
x1 = trunc(Int64, 10.3);


struct carajo 
    test::Int64;
end;

varr = carajo (64);
v2 = varr.test;

#if mayuscula == "HOLA" 
#    function err () 
#    end;
#    #error ->m = uppercase(false);
#    println("esto ya no jala");
#
#end;
sho = 20::Float64;
sho = 20::Float64;
sho = 20::Float64;

# tests(true);

println("FIN");
#val = !10;
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

#function sum(val1, val2) 
#
#    #println("conteo:", val1); 
#    val1 = val1 + 1;
#    #println("Luego de incrementar:", val1);
#    if val1 > val2
#        println("Aqui solo deberia ingresar una vez================", val1, " ", val2);
#        circ = circulo("azul", true);
#        val = circ.contento;
#        return 20; #hubieron 2 return seguidos.. cuidado
#    else 
#        #println("Con que valor va a llamar a otra funcion ==============>", val1);
#        res = sum(val1, val2);
#        #println("Que valor tendra aqui", res);
#        println("Aqui deberia ser 1 menos creo:", val1, res);
#    end;
#
#end;
#val = 0;
#println("El verdade",sum(2, 5));
#
#function f1 ()
#
#    if true 
#        println("PORQUE ENTRA DOS VECES AQUI =================================================");
#        return 10;
#    end; 
#    
#end; 
#
#
#function f2() 
#    println("Este mensaje fijo funciona");
#    f1(); 
#    #println("Este ya no va a funcionar",f1());
#end; 

#println(f2());
# println("Que putas mano?:",sum(2, 10)); esta sentencia no esta funcionando, las funciones no estan retornando nada
