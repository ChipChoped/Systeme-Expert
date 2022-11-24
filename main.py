from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser
from Context import Context
import logging

if __name__ == "__main__":

    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    print("test du lexer, entrez ce que vous voulez !")

    custom = CustomParser(Context())
    lexer = CustomLexer().lexer
    while 1:
        try:
            s = input('test > ')
        except EOFError:
            break
        if not s:
            continue
        custom.parser.parse(s)
        logging.info("Etat du context : \n"+str(custom.context))
    # result = custom.parser.parse(prompt)
    