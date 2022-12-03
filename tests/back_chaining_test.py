import logging

from Moteur import Moteur
from Context import Context
from Datatypes import Element
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser


class TestBackChaining:
    def test_success(self):
        moteur = Moteur(Context())
        custom = CustomParser(moteur)
        lexer = CustomLexer().lexer
        custom.parser.parse('load("ressources/ex2")')
        logging.info("État du context : \n" + str(moteur.context))
        hypotheses = moteur.chainageArriere(['BondChampagne', 'ChateauEarl', 'HonestHenryAppleWine', 'ToeLakesRose', 'DosEquis', 'Coors', 'Glops', 'CarrotJuice', 'Water'])
        right_hypotheses = [Element(hypothesis, True) for hypothesis in ['HonestHenryAppleWine', 'DosEquis', 'Coors', 'Water']]
        assert hypotheses == right_hypotheses
