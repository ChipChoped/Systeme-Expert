import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule, Boolean, EnumElem
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


def test_forward_chaining_boolean(base_context):
    base_context.parser.parse('load("ressources/ex2")')
    added_facts, used_rules = base_context.moteur.chainageAvant(
        [Boolean('BondChampagne', True), Boolean('ChateauEarl', True), Boolean('HonestHenryAppleWine', True), Boolean('ToeLakesRose', True), Boolean('DosEquis', True),
            Boolean('Coors', True), Boolean('Glops', True), Boolean('CarrotJuice', True), Boolean('Water', True)])
    
    # print("added facts : ")
    # print(added_facts)

    # print("used_rules :")
    # print(used_rules)

    # print(base_context.moteur.context.rules)

    
    right_added_facts = [Boolean('Wine', True), Boolean('CheapWine', True), Boolean('HonestHenryAppleWine', True)]
    rights_used_rules = [base_context.moteur.context.rules['B11'], base_context.moteur.context.rules['WineRules'].rule_list[1], base_context.moteur.context.rules['B3']]
    
    assert added_facts == right_added_facts
    assert used_rules == rights_used_rules

def test_forward_chaining_enum(base_context):
    base_context.parser.parse('load("ressources/ex2_zp")')
    added_facts, used_rules = base_context.moteur.chainageAvant()
    
    print("added facts : ")
    print(added_facts)

    # print("used_rules :")
    # print(used_rules)

    print("context :")
    print(base_context.moteur.context)

    
    right_added_facts = [Boolean('Wine', True), EnumElem('chosenBeverage', {'CheapWine' : Boolean('CheapWine', True)}), Boolean('HonestHenryAppleWine', True)]
    rights_used_rules = [base_context.moteur.context.rules['B11'], base_context.moteur.context.rules['WineRules'].rule_list[1], base_context.moteur.context.rules['B3']]
    
    assert added_facts == right_added_facts
    assert used_rules == rights_used_rules
