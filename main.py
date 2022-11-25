from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser
from Moteur import Moteur
from Context import Context
import logging

if __name__ == "__main__":

    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    print("test du lexer, entrez ce que vous voulez !")

    moteur = Moteur(Context())
    custom = CustomParser(moteur)
    lexer = CustomLexer().lexer
    while 1:
        try:
            s = input('test > ')
        except EOFError:
            break
        if not s:
            continue
        custom.parser.parse(s)
        logging.info("Etat du context : \n"+str(moteur.context))
    # result = custom.parser.parse(prompt)
    