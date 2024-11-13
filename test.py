from lex import lexer
from pars import Parser


def analyze_code(code):
    try:
        tokens = lexer(code)
        print("Tokens:", tokens)
        parser = Parser(tokens)
        parser.parse()
        print("Successful")
    except SyntaxError as e:
        print("Parsing error:", e)


codes = ['''
    program var a: %; 
    begin 
      a := 0;
      writeln a;
    end
    ''', '''
    program var a: %; 
    begin 
      a := 10; 
      if (a > 5) 
        writeln 'a больше 5'
      else 
        writeln 'a меньше или равно 5'; 
    end
    ''', '''
    program var a, b, s, i: %;
    begin
      readln(a, b);
      sum := 0;
      for i := a to b step 1 do
      begin
        s := s + i;
      end;
      writeln('Сумма чисел от ', a, ' до ', b, ' равна ', s);
    end
    ''']


for elem in codes:
    analyze_code(elem)