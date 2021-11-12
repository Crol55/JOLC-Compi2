#function swap(i::Int64, j::Int64, arr) 
#    temp = arr[i]::Int64;
#    arr[i] = arr[j];
#    arr[j] = temp;
#end;
#
#function bubbleSort(arr)
#    for i in 0:(length(arr) - 1)
#        for j in 1:(length(arr) - 1)
#            if(arr[j] > arr[j + 1])
#                swap(j, j+1, arr);
#            end;
#        end;
#    end;
#end;
#
#function insertionSort(arr) 
#
#    for i in 2:length(arr)
#        j = i;
#        temp = arr[i];
#        while(j > 1 && arr[j - 1] > temp)
#            arr[j] = arr[j-1];
#            j = j - 1;
#        end;
#        arr[j] = temp;
#    end;
#
#end;
#
#arreglo = [32,7*3,7,89,56,909,109,2,9,9874^0,44,3,820*10,11,8*0+8,10];
#bubbleSort(arreglo);
#println("BubbleSort => ",arreglo);
#
#arreglo = [32,7*3,7,89,56,909,109,2,9,9874^1,44,3,820*10,11,8*0+8,10];
#arreglo[1] = arreglo[2]^0;
#insertionSort(arreglo);
#print("InsertionSort => ",arreglo);

#println(15 + 2 * 10.35 - 10*25);
#println(10,20,30);
#print(false, true);
#println(nothing);
#println('M');
#println( 10 > 1.2 == false);
#println( true == false);
#println( true == (5 < 2));
#println( 1 < 10 || 1 < 5 );
#println( true && true && (50 && 70 && 80));

#val1 = 10*25-7;
#val2 = 0;
#println(val1);
#println(val2);
#println("");
#println("Hola mundo desde este puto compilador XD");

#if (val2 == 10)
#   print("es diez");
#elseif (val2 == 20)
#    print("es veinte");
#else 
#    print("es indefinido");
#end;

#val2 = val1;

#while (val2 < 2)
#end;

local val = 1;

#println(val);
local val = "hi"; 
val2 = 10;
val2 = "jiji";
println(val);
println(val2);

global xx = 25;

if (xx == 25)
    local x = 1; 
    xx = 30;
end;

print(xx);

 # =====================

 struct Actor
    nombre:: String;
    edad:: Int64;
end;

struct Contrato 
    actor::Actor;
end;

carl = Contrato( Actor("carlos", 28) );

println(  carl.actor.edad, carl.actor.nombre );
#println( carl);

