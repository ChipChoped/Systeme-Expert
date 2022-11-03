from ply import lex as lexer

reserved = {'ET' : 'ET', 'NON' : 'NON'}

tokens = [
    'IMPLIQUE', 'MOT'
 ] + list(reserved.values())


class CustomLexer(object):

    def generateLexer():
        t_IMPLIQUE = r'=>'
        t_ignore  = ' \t'

        def t_MOT(t):
            r'[a-zA-Z]+'
            t.type = reserved.get(t.value,'MOT')    # Check for reserved words
            return t

        def t_error(t):
            print(f"Illegal character ({t.value})")
            t.lexer.skip(1)

        return lexer.lex()

