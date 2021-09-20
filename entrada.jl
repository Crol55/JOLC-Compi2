struct Actor
    nombre:: String;
    edad:: Int64;
end;

struct Pelicula 
    nombre::String;
    posicion::Int64;
end;

struct Contrato
    inutil::Actor;
    peli::Pelicula;
end;

struct algo 
    prue::Contrato;
end;

actor1 = Actor("malelin", 28);
movie = Pelicula("God of war", 20);

contract = Contrato(actor1, movie);
println(contract);

nuevita = algo(contract);
println(nuevita);
# Prueba para arrays
array = [10,20,[true], "hola"];
println(array[4]);
array [4] = [10];
println(array[4]);

# prueba a sentencias de transferencia
println("");
println("=======================================================================");
println("=============================TRANSFERENCIA=============================");
println("=======================================================================");

a = -1;
while (a < 5)
    global a = a + 1;
    if a == 3
        print("a");
        continue;
    elseif a == 4
        println("b");
        break;
    end;

    print("El valor de a es: ", a, ", ");
end;

println("Se debió imprimir");
# Prueba, true debe aparecer en minuscula
println(true);

# Testeando acceso por operador punto
println(actor1.edad.val.val);