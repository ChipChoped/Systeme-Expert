from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser

import readline # GARDER CET IMPORT

from CoherenceExceptions import *
from ParsingException import *
from Moteur import Moteur
from Context import Context
import logging

if __name__ == "__main__":

    logging.basicConfig(encoding='utf-8', level=logging.WARNING)

    # print("test du lexer, entrez ce que vous voulez !")

    moteur = Moteur(Context())
    custom = CustomParser(moteur)
    lexer = CustomLexer().lexer
    custom.c_help()
    while 1:
        try:
            s = input('m0+ > ')
        except EOFError:
            break
        if s == "\n":
            continue
        try :
            custom.parser.parse(s)
        except RuleCoherenceException as e:
            custom.handle_rule_coherence_exception(e)
        except Exception as e : 
            custom.handle_generic_exception(e)

        logging.info("Etat du context : \n"+str(moteur.context))
    # result = custom.parser.parse(prompt)
    