procedure proce(n : integer)
begin 
    writeln('procedura')
end;

function func(n:integer)
begin 
    writeln('funkcija')
end;

var
   a: integer;
   b: real;
   c: boolean;
   d: char;
   e: string;
   f: void;
   vector : array [ 0..24] of real;

begin
   a := 10;
   p := 5;
   b := 10.5;
   c := true;
   d := 'c';
   e := 'String'
   adivp := a div p;
   amodp := a mod p;
   axorp := a xor p;
   if (a = 10) and (p = 5) Then writeln(a);
   if (a = 10) or (p = 5) Then writeln(a);
   if not (a = 10) Then writeln(a)
   else witeln(p);
   repeat
        break;
        continue;
      writeln('value of a: ', a);
      a := a + 1;
      if a = 15 do 
      begin 
        exit;
      end;
   until a = 20;
   for i:= 1 to 10 do
   begin 
        writeln(i);
    end;
   while a < 6 do
    begin
      writeln (a);
      a := a + 1
    end;
    x = abs(a);
    x = round(a);
    x = inc(a);
    x = dec(a,2);
    
end.
