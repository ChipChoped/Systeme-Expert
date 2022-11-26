from Moteur import Moteur
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser
from Datatypes import Context
import logging

if __name__ == "__main__":

    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    print("Alimentation de la base de connaissance :\n")

    custom = CustomParser(Context())
    lexer = CustomLexer().lexer
    moteur = Moteur()

    while 1:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        custom.parser.parse(s)
        logging.debug("État de la base de connaissance : \n" + str(custom.context))
    # result = custom.parser.parse(prompt)

    if custom.context.hypotheses:
        right_hypotheses = moteur.chainageArriere(custom.context.facts, custom.context.rules, custom.context.hypotheses)
        print("Hypothèses corrects :")
        print(right_hypotheses)
