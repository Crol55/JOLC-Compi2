struct Personaje
    nombre:: String;
    color:: String;
end;

struct Juego 
    nombre::String;
    horas::Int64;
end;

struct Compania
    personaje::Personaje;
    juego::Juego;
end;

function crear(personaje::Personaje, juego::Juego)::Compania
    return Compania(personaje,juego);
end;


function crearPersonaje(nombre::String, color::String)::Personaje
    return Personaje(nombre,color);
end;

function crearJuego(nombre::String, horas::Int64)::Juego
    return Juego(nombre,horas);
end;


function imprimir(compania::Compania)::nothing
    per1 = compania.personaje;
    game = compania.juego;
    println("Personaje: ", per1.nombre, "   Color: ", per1.color);
    #println("Juego: ", game.nombre, "   Horas: ", game.horas);  
    
end;

personaje1 = crearPersonaje("Mario", "Rojo");
juego1     = crearJuego("Mario Kart", 3);
# Compania XD
comp1 = crear(personaje1, juego1);

println(personaje1, juego1, comp1);
println(personaje1.nombre);

# imprimiendo desde funcion
imprimir(comp1);
