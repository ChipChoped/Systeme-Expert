from ply import lex as lexer

reserved = {'ET': 'ET', 'NON': 'NON'}


class CustomLexer(object):
    tokens = [
        'IMPLIQUE', 'MOT', 'OPEN_PAR', 'CLOSE_PAR', 'COMMA', 'DEUX_POINTS', 'OPEN_BRACK', 'CLOSE_BRACK', 'STRING', 'GREATER'
    ] + list(reserved.values())

    t_IMPLIQUE = r'=>'
    t_ignore = ' \t\n'
    t_OPEN_PAR = r'\('
    t_CLOSE_PAR = r'\)'
    t_COMMA = r','
    t_DEUX_POINTS = r':'
    t_OPEN_BRACK = r'\['
    t_CLOSE_BRACK = r'\]'
    t_GREATER = r'>'


    def t_MOT(self, t):
        r'[0-9a-zA-Z]+'
        t.type = reserved.get(t.value, 'MOT')    # Check for reserved words
        return t

    def t_STRING(self, t):
        r'".*"'
        t.value = t.value[1:-1]
        return t
        

    def t_error(self, t):
        print(f"Illegal character ({t.value})")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lexer.lex(module=self)
