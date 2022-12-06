import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import Element, ConcreteRule, Boolean, EnumElem, Hypothesis, ConcreteRule, Constraint, OperatorTypes
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

    objective = Hypothesis("h1",[
    ConcreteRule([Constraint(Boolean('BondChampagne', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('ChateauEarl', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('HonestHenryAppleWine', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('ToeLakesRose', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('DosEquis', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('Coors', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('Glops', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('CarrotJuice', True), OperatorTypes.EQUALS)], [], ''), 
    ConcreteRule([Constraint(Boolean('Water', True), OperatorTypes.EQUALS)], [], ''), ])

    context = base_context.moteur.chainageAvant(objective)
    
    moteur_correction = Moteur(Context())
    lexer_correction = CustomLexer().lexer
    correction = CustomParser(moteur_correction)
    correction.parser.parse('load("ressources/ex2_final_context")')
        
    assert context.facts == correction.moteur.context.facts
    assert context.rules == correction.moteur.context.rules

def test_forward_chaining_enum_no_objective(base_context):
    base_context.parser.parse('load("ressources/ex2_zp")')

    print("base context :")
    print(base_context.moteur.context)
    
    context = base_context.moteur.chainageAvant(base_context.moteur.context.hypothesis["H1"])

    print("added context :")
    print(context)

    moteur_correction = Moteur(Context())
    lexer_correction = CustomLexer().lexer
    correction = CustomParser(moteur_correction)
    correction.parser.parse('load("ressources/ex2_zp_final_context")')
        
    assert context.facts == correction.moteur.context.facts
    assert context.rules == correction.moteur.context.rules
