from ply import lex as lexer

reserved = {'ET': 'ET', 'NON': 'NON'}


class CustomLexer(object):
    tokens = [
        'NUMBER', 'IMPLIQUE', 'OPEN_PAR', 'CLOSE_PAR', 'COMMA', 'DEUX_POINTS', 
        'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 
        'OPEN_BRACK', 'CLOSE_BRACK', 'STRING', 'GREATER', 'EQUALS', 'EQUALITY', 
        'MOT', 'ID'
    ] + list(reserved.values())


    # t_NUMBER = r'[0-9]+'
    t_IMPLIQUE = r'=>'
    t_ignore = ' \t\n'
    t_OPEN_PAR = r'\('
    t_CLOSE_PAR = r'\)'
    t_COMMA = r','
    t_DEUX_POINTS = r':'
    t_OPEN_BRACK = r'\['
    t_CLOSE_BRACK = r'\]'
    t_GREATER = r'>'
    t_EQUALS = r'='
    t_EQUALITY = r'=='
    t_GREATER_EQUAL = r'>='
    t_LESS = r'<'
    t_LESS_EQUAL = r'<='


    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_MOT(self, t):
        r'[0-9a-zA-Z]+'
        if(t.value in reserved):
            t.type = reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def t_STRING(self, t):
        r'".*"'
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        t.lexer.skip(1)
    
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def __init__(self):
        self.lexer = lexer.lex(module=self)
