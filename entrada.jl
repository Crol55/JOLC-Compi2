

#local x = 6 % 4 * 5+4 ;
#global x = 6 % 4 * 5+4 ;
#local x = 6 % 4 * 5+4.3 ;
#x = 6 % 4 * 5+4::Int64 ;
#var = true; 
#var = false;
#var = "hola mundo";
#var = 'c';
#z = nothing;
#z = [];
#z = [20, 10];
#val = "val" + " nuevo";
#val = "valuees:" * " nuevo";
#val = "valuees:" ^4;
#val = uppercase("valuees:" ^4);
#val = lowercase("TIGRE") + uppercase("tigre");
#val = parse(Float64, "-20.5");
#val = trunc(Int64, 0.0999);
#val = float(24);
#val = string( 2 *5);
#val = typeof(true);
#
#val = sin(0.5235);
#val = cos(0.5235);
#val = tan(3.4);
#val = log10(5);
#val = log(10, 5);
#val = sqrt(25);
#
#val = 20 == 20;
#val = 20 != 10;
#val = 20 > 20;
#val = 20 < 20;
#val = 20 >= 20;
#val = true == true;

#val = !(false && true);
#val = -10*20;
#=val = -25^(69-33*2)+22-32*2-33^(-48+48)::Int64;
val2 =  10 < 20 || 10 >=11;
local val3 = 10::Int64; 
global val4 = 23.0::Float64; 
test = val4;=#

#= 
val = 100;
function vals(tipado::Int64, val1, val2)
    
    val = tipado * val1;
    esmayor = false; 
    if (val >= 200)
        println("Si es mayor a 200");
        local esmayor = true;
    else
        println("No es mayor a 200");
    end; 
    println("Testeo de ambito ", esmayor);
end;

vals(10, 20 , false);
println("El valor de Val es:", val);=#
#=
cond = 10; 
while (cond >= 10) 
    local val = 10;
    cond = cond -1 ;

    return 2;
    cond = cont -5;

    println("El valor de cond es:", cond);
    
end; 

println("El valor de cond global es:", cond);=#
#=
val = 100;
function vals(tipado::Int64, val1, val2)
    #return;
    #return 9* tipado;
    #return tipado * 3;
    
    tipado = 23.5;
    val = 5;
    println("El valor en la fun:", tipado * val);
    #return;
    #function invalid () end;
    #while true 
    #    break;
    #end;
end;

=#

  
println("Funciones nativas aritmeticas");
# log(base, numero)
println(log(2, 4));     # 2.0
println(log(9, 135));   # 2.2324867603589635
# log10()
println(log10(2000));   # 3.3010299956639813
println(log10(512));    # 2.709269960975831
# trigonometricas
println(sin(67/360*2*3.14));    # 0.9202730580752193
println(cos(67/360*2*3.14));    # 0.39127675446016985
println(tan(67/360*2*3.14));    # 2.351974778938468
# sqrt
println(sqrt(2^4));     # 4.0
println(sqrt(1258));    # 35.4682957019364

println("Operaciones con cadenas");
println("para" * "caidismo");   # paracaidismo
println("Holaaa"^5);    # HolaaaHolaaaHolaaaHolaaaHolaaa

println(uppercase("mayuscula"));    # MAYUSCULA
println(lowercase("MINUSCULA"));    # minuscula

function mulNumbers(val1,  val2)

    return val1 * val2; 
end;

function main ()

    val1 = 10; 
    val2 = 20;

    resultado = mulNumbers(val1, val2); 
    #=while (val1 < val2)
        println(val1); 

        val1 = val1 + 1 ;
    end;=# 

    println("El resultado de la multiplicacion es:", resultado);

end; 

#main();
# ========================= 2do testeo
x = 8200::Int64;

function suma(a,b)
  global x = a + b;
end;

x = 15::Int64;

function numero()

    local x = 80; #local de la funcion
    y = 0;
    while (y < 10)
        local x = 9; #local del ciclo
        y = y + 1;
        println(x); #9
    end;
    println(x); #80
end;
numero();
println(x); #15