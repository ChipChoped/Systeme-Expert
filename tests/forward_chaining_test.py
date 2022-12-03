import logging

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser


class TestForwardChaining:
    moteur = Moteur(Context())
    custom = CustomParser(moteur)
    lexer = CustomLexer().lexer

    def test_success(self):
        self.custom.parser.parse('load("ressources/ex2")')
        logging.info("État du context : \n" + str(self.moteur.context))
        added_facts, used_rules = self.moteur.chainageAvant(
            ['BondChampagne', 'ChateauEarl', 'HonestHenryAppleWine', 'ToeLakesRose', 'DosEquis',
             'Coors', 'Glops', 'CarrotJuice', 'Water'])
        right_added_facts = '[Wine, CheapWine, HonestHenryAppleWine]'
        rights_used_rules = '[B11 : GuestSophisticated -> Wine, B10 : Wine -> CheapWine, B3 : CheapWine, EntreeChicken, NOT GuestWellLiked -> HonestHenryAppleWine]'
        print(added_facts)
        assert added_facts.__str__() == right_added_facts
        assert used_rules.__str__() == rights_used_rules

    def test_fail(self):
        pass