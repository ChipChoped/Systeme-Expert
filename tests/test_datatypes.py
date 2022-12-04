import logging
import pytest

from Moteur import Moteur
from Context import Context
from Datatypes import OperatorTypes, Constraint, Element, ConcreteRule, Boolean, Number, EnumElem, VariableTypes
from parser.CustomLexer import CustomLexer
from parser.CustomParser import CustomParser



# @pytest.fixture
# def base_context():
#     moteur = Moteur(Context())
#     lexer = CustomLexer().lexer
#     custom = CustomParser(moteur)
#     return custom


def test_boolean_conflict():
    b1 = Boolean("test", True)
    b2 = Boolean("test", False)
    assert b1.conflict(b2)

    b1 = Boolean("test", True)
    b2 = Boolean("test", True)
    assert not b1.conflict(b2)
   
    b1 = Boolean("tst", True)
    b2 = Boolean("test", True)
    assert not b1.conflict(b2)

def test_boolean_conflicts():
    b1 = Boolean("test", True)
    assert b1.conflicts([Boolean('a', False), Boolean('b', True), Boolean('test', False)])
    assert not b1.conflicts([Boolean('a', False), Boolean('b', True)])

def test_number_conflict():
    b1 = Number("test", 2)
    b2 = Number("test", 3)
    assert b1.conflict(b2)

    b1 = Number("test", 2)
    b2 = Number("test", 2)
    assert not b1.conflict(b2)
   
    b1 = Number("test", 2)
    b2 = Number("tet", 2)
    assert not b1.conflict(b2)

def test_enum_conflict():
    b1 = EnumElem("test", "hello")
    b2 = EnumElem("test", "hella")
    assert b1.conflict(b2)

    b1 = EnumElem("test", "salut")
    b2 = EnumElem("test", "salut")
    assert not b1.conflict(b2)
    
    b1 = EnumElem("test", "salut")
    b2 = EnumElem("tet", "hello")
    assert not b1.conflict(b2)

def test_variable_type():
    assert VariableTypes.BOOLEAN != VariableTypes.NUMBER

def test_constraint_nok():
    with pytest.raises(Exception) as e_info:
        c1 = Constraint(Boolean("name", True), OperatorTypes.GREATER)

def test_constraint_bool():
    c1 = Constraint(Boolean("name", True), OperatorTypes.EQUALS)
    assert c1.str_condensed() == 'name_equal_True'
    c2 = Constraint(Boolean("name", False), OperatorTypes.EQUALS)
    assert c2.str_condensed() == 'name_equal_False'

def test_constraint_number():
    n1 = Constraint(Number("name", 3), OperatorTypes.GREATER)
    assert n1.str_condensed() == 'name_greater_3'
    n2 = Constraint(Number("name", 3), OperatorTypes.GREATER_OR_EQUAL)
    assert n2.str_condensed() == 'name_greaterOrEqual_3'

def test_contraint_bool_validity():
    c1 = Constraint(Boolean("name", True), OperatorTypes.EQUALS)
    b2 = Boolean("autre", True)
    assert c1.satisfy(b2)

    b3 = Boolean("encore_autre", False)
    assert not c1.satisfy(b3)

def test_contraint_number_validity():
    c1 = Constraint(Number("name", 3), OperatorTypes.EQUALS)
    c2 = Constraint(Number("name", 2), OperatorTypes.EQUALS)
    c3 = Constraint(Number("name", 2), OperatorTypes.GREATER)

    n1 = Number("autre", 3)
    assert c1.satisfy(n1)
    assert not c2.satisfy(n1)
    assert c3.satisfy(n1)

def test_constraint_satisfiable():
    c1 = Constraint(Number("name", 3), OperatorTypes.EQUALS)
    facts = {"truc" : Number("truc", 3),"name" : Number("name",3)}
    assert c1.satisfiable(facts)
    
    facts = {"truc" : Number("truc", 3),"name" : Number("name",4)}
    assert not c1.satisfiable(facts)