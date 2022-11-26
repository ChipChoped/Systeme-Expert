from ply import lex as lexer

reserved = {'ET': 'ET', 'NON': 'NON'}


class CustomLexer(object):
    tokens = [
        'IMPLIQUE', 'MOT', 'ID', 'OPEN_PAR', 'CLOSE_PAR', 'COMMA'
    ] + list(reserved.values())

    t_IMPLIQUE = r'=>'
    t_ignore = r' \t'
    t_OPEN_PAR = r'\('
    t_CLOSE_PAR = r'\)'
    t_COMMA = r','

    
    def t_MOT(self, t):
        r'[a-zA-Z]+'
        t.type = reserved.get(t.value, 'MOT')    # Check for reserved words
        return t

    def t_error(self, t):
        print(f"Illegal character ({t.value})")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lexer.lex(module=self)
