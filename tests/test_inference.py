import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser



@pytest.fixture
def base_context():
    moteur = Moteur(Context())
    lexer = CustomLexer().lexer
    custom = CustomParser(moteur)
    return custom


def test_backward_chaining(base_context):
    base_context.parser.parse('load("ressources/ex2")')
    hypotheses = base_context.moteur.chainageArriere(
        ['BondChampagne', 'ChateauEarl', 'HonestHenryAppleWine', 'ToeLakesRose', 'DosEquis',
            'Coors', 'Glops', 'CarrotJuice', 'Water'])
    right_hypotheses = [Element(hypothesis, True) for hypothesis in ['HonestHenryAppleWine', 'DosEquis', 'Coors', 'Water']]
    assert hypotheses == right_hypotheses


def test_forward_chaining(base_context):
    base_context.parser.parse('load("ressources/ex2")')
    added_facts, used_rules = base_context.moteur.chainageAvant(
        ['BondChampagne', 'ChateauEarl', 'HonestHenryAppleWine', 'ToeLakesRose', 'DosEquis',
            'Coors', 'Glops', 'CarrotJuice', 'Water'])
    right_added_facts = '[Wine, CheapWine, HonestHenryAppleWine]'
    rights_used_rules = '[B11 : GuestSophisticated -> Wine, B10 : Wine -> CheapWine, B3 : CheapWine, EntreeChicken, NOT GuestWellLiked -> HonestHenryAppleWine]'
    
    print("added facts : ")
    print(added_facts)
    
    assert added_facts.__str__() == right_added_facts
    assert used_rules.__str__() == rights_used_rules

