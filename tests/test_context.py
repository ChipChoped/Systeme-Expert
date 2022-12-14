import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import *
from CoherenceExceptions import *
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser



@pytest.fixture
def base_context():
    moteur = Moteur(Context())
    lexer = CustomLexer().lexer
    custom = CustomParser(moteur)
    return custom


def test_add_fact_normal(base_context):
    b1 = Boolean("test", True)
    base_context.moteur.context.addFact(b1)
    assert base_context.moteur.context.facts == {'True' : Boolean('True', True), b1.name : b1}
    
    n1 = Number("test2", 1)
    base_context.moteur.context.addFact(n1)
    assert base_context.moteur.context.facts == {'True' : Boolean('True', True), b1.name : b1, n1.name : n1}
    
    e1 = Number("test3", "test")
    base_context.moteur.context.addFact(e1)
    assert base_context.moteur.context.facts == {'True' : Boolean('True', True), b1.name : b1, n1.name : n1, e1.name : e1}
 
def test_add_fact_conflict_type(base_context):
    b1 = Boolean("test", True)
    base_context.moteur.context.addFact(b1)
    assert base_context.moteur.context.facts == {'True' : Boolean('True', True), b1.name : b1}

    with pytest.raises(Exception) as e_info:
        e1 = EnumElem("test", "test")
        base_context.moteur.context.addFact(e1)

def test_add_fact_conflict_type(base_context):
    b1 = Boolean("test", True)
    base_context.moteur.context.addFact(b1)
    assert base_context.moteur.context.facts == {'True' : Boolean('True', True), b1.name : b1}

    with pytest.raises(Exception) as e_info:
        b2 = Boolean("test", False)
        base_context.moteur.context.addFact(b2)


def test_add_rule(base_context):
    r1 = ConcreteRule([Constraint(Number("test", 2), OperatorTypes.GREATER)], [Number("test2",3)], 'r1')
    base_context.moteur.inputRule(r1)
    
    with pytest.raises(TypeCoherenceException) as e_info:
        r2 = ConcreteRule([Constraint(Boolean("test", True), OperatorTypes.EQUALS)], [Number("test2",3)], 'r1')
        base_context.moteur.inputRule(r2)
   