from Modules.Lexer import *
from Modules.Parser import *
from Modules.Grapher import *
from Modules.Symbolizer import *
from Modules.Generator import *
from Modules.Runner import *

test_id = 1
folder_id = '10'
#path = f'pas/test{test_id}.pas'
path = f'{folder_id}/src.pas'

with open(path, 'r') as source:
    text = source.read()

    lexer = Lexer(text)
    tokens = lexer.lex()
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()
    grapher = Grapher(ast)
    img = grapher.graph()

    # symbolizer = Symbolizer(ast)
    # symbolizer.symbolize()

    # print(ast)

    # generator = Generator(ast)
    # code = generator.generate('main.py')
    #
    # !cat '{code}' # prikazivanje generisanog koda
    # !python3 '{code}' #pokretanje generisanog koda
    #
    # runner = Runner(ast)
    # runner.run()
    Image(img)

