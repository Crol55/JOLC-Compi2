

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

#function sumas () 
#    continue;
#end; 
#
#function x () 
#    val50 = 10;
#end;
val = 100;
function vals(tipado::Int64, val1, val2)
    #return;
    #return 9* tipado;
    #return tipado * 3; 
    print("Hola mundo");
    #return;
    #function invalid () end;
    #while true 
    #    break;
    #end;
end;

vals(10, 20 , false);
#vals(5, 20 , false);

#function testeo (tipado, notipado)
#    
#    break;
#end;
#val = -25^(69-33*2)+22-32*2-33^(-48+48);
#x = 6 * 4 -3.5 ;
#x = 6 * 4 +1 ;