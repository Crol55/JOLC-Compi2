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
