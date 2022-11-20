from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser
from Datatypes import Context
import logging

if __name__ == "__main__":

    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    print("Alimentation de la base de connaissance :")

    custom = CustomParser(Context())
    lexer = CustomLexer().lexer
    s = ""

    while not s == 'FIN':
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        custom.parser.parse(s)
        logging.debug("État la base de connaissance : \n" + str(custom.context))
    # result = custom.parser.parse(prompt)
    